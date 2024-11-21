import os
import shutil
import argparse
import xml.etree.ElementTree as ET
from xml.dom import minidom

def move_drivers(base_source_dir, base_output_dir, target_silicon, model_number):

    # Parse XML
    tree = ET.parse('Config.xml')
    root = tree.getroot()

    bold = "\033[1m"
    bold_blue = "\033[1;34m"
    yellow = "\033[93m"
    reset = "\033[0m"

    # For now search all Driver elements at all levels
    for driver in root.findall('.//Driver'):
        source_name = driver.get('SrcDir').replace("$(silicon)", target_silicon)
        output_directory = driver.get('OutDir').replace("$(SoC)", model_number)

        # Combine input path + driver directory
        full_source_dir = os.path.join(base_source_dir, source_name)
        full_output_dir = os.path.join(base_output_dir, output_directory)

        # Check if input driver directory exists
        if not os.path.exists(full_source_dir):
            print(f"{bold_blue}Notice:{reset} Driver directory '{source_name}' not found. Skipping...")
            continue

        # Create output directory if it doesn't exist
        os.makedirs(full_output_dir, exist_ok=True)

        # Move files from source to output directory
        for item in os.listdir(full_source_dir):
            source_item = os.path.join(full_source_dir, item)
            output_item = os.path.join(full_output_dir, item)
            shutil.move(source_item, output_item)

        os.rmdir(full_source_dir)
        print(f"Moved contents of '{source_name}' to '{output_directory}'")

    # Check if there are any left-over drivers in source dir
    remaining_drivers = [item for item in os.listdir(base_source_dir) if os.path.isdir(os.path.join(base_source_dir, item))]
    if remaining_drivers:
        print(f"\n{bold}{yellow}Warn:{reset} The following drivers were not moved from '{base_source_dir}':")
        for leftover in remaining_drivers:
            print(f" - {leftover}")


# Generate driver definitions xml
def prettify(element):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def generate_definitions(comp_path, output_xml):
    # Create root FeatureManifest element with attributes
    feature_manifest = ET.Element("FeatureManifest", {
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
        "xmlns": "http://schemas.microsoft.com/embedded/2004/10/ImageUpdate",
        "Revision": "1",
        "SchemaVersion": "1.3"
    })

    # Create "Drivers" and "BaseDriverPackages" nested elements
    drivers = ET.SubElement(feature_manifest, "Drivers")
    base_driver_packages = ET.SubElement(drivers, "BaseDriverPackages")

    # Walk through the directory structure
    for subdir, _, files in os.walk(comp_path):
        for file in files:
            if file.endswith(".inf"):
                # Construct full path and filename
                inf_path = os.path.relpath(subdir, start=comp_path)
                modelnumber = f"QC{args.modelnumber}"
                inf_full_path = f"$(mspackageroot)\\components\\{modelnumber}\\{inf_path}".replace("/", "\\")
                inf_name = file
                inf_id = os.path.splitext(inf_name)[0]  # ID is the name without extension

                # Create XML entry for each .inf file inside BaseDriverPackages
                driver_package = ET.SubElement(base_driver_packages, "DriverPackageFile")
                driver_package.set("Path", inf_full_path)
                driver_package.set("Name", inf_name)
                driver_package.set("ID", inf_id)

    # Pretty-print the XML for line breaks and formatting
    pretty_xml_as_string = prettify(feature_manifest)

    # Write the pretty XML string to the output file
    with open(output_xml, "w", encoding="utf-8") as f:
        f.write(pretty_xml_as_string.split("?>", 1)[-1].strip())

# Command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""This script organizes extracted Windows drivers from CAB files and generates XML driver definitions.
The script looks for the source directory defined in the Config.xml and then moves
it's contents to an organized directory specified in XML.

Example command:
    python main.py --input ./Drivers --output ./Output --silicon 7280

""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-i", "--input", required=True, help="Input directory containing extracted CAB folders")
    parser.add_argument("-o", "--output", default="Output", help="Output directory of organized files. Default: Output")
    parser.add_argument("-s", "--silicon", required=True, help="Target silicon. Examples: 7180, 7280, 8180")
    parser.add_argument("-m", "--modelnumber", help="SoC model number. Defaults to --silicon value")

    args = parser.parse_args()

    # Defaults for modelnumber arg
    if args.modelnumber is None:
        args.modelnumber = args.silicon

    comp_path = os.path.join(args.output, f"QC{args.modelnumber}")
    output_xml = os.path.join(args.output, f"{args.modelnumber}.xml")
    os.makedirs(os.path.dirname(output_xml), exist_ok=True)

    # Call directory-structurizer and xml-gen functions with the provided arguments
    move_drivers(args.input, args.output, args.silicon, args.modelnumber)
    generate_definitions(comp_path, output_xml)
