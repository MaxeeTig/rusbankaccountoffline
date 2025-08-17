import xml.etree.ElementTree as ET
import json
import argparse
import os

def convert_bic_xml_to_json(input_file, output_file):
    """
    Converts BIC XML file to simplified JSON format
    Args:
        input_file: path to input XML file
        output_file: path to output JSON file
    """
    try:
        # Parse XML file
        tree = ET.parse(input_file)
        root = tree.getroot()

        # Extract BIC entries
        bic_data = {}
        ns = {'ns': 'urn:cbr-ru:ed:v2.0'}  # XML namespace
        
        for entry in root.findall('.//ns:BICDirectoryEntry', ns):
            bic = entry.get('BIC')
            participant = entry.find('ns:ParticipantInfo', ns)
            
            if bic and participant is not None:
                bank_name = participant.get('NameP')
                if bank_name:
                    bic_data[bic] = bank_name

        # Save as JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(bic_data, f, ensure_ascii=False, indent=2)

        print(f"Conversion successful!")
        print(f"Input: {os.path.abspath(input_file)} ({os.path.getsize(input_file)/1024:.1f} KB)")
        print(f"Output: {os.path.abspath(output_file)} ({os.path.getsize(output_file)/1024:.1f} KB)")
        print(f"Converted {len(bic_data)} BIC entries")

    except Exception as e:
        print(f"Error during conversion: {str(e)}")

if __name__ == "__main__":
    # Set up command line arguments
    parser = argparse.ArgumentParser(
        description='Convert BIC XML directory to simplified JSON format'
    )
    parser.add_argument(
        '-i', '--input', 
        default='bic_directory.xml',
        help='Input XML file (default: bic_directory.xml)'
    )
    parser.add_argument(
        '-o', '--output', 
        default='bic_directory.json',
        help='Output JSON file (default: bic_directory.json)'
    )

    args = parser.parse_args()

    # Run conversion
    convert_bic_xml_to_json(args.input, args.output)