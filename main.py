"""
XMind Converter - Main Entry Point
Converts XMind files to various formats (Markdown, CSV, etc.)
"""
import os
import argparse
import logging
from pathlib import Path
from xmind_parser import XMindMapAccesser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def convert_to_markdown(xmind_file_path: str, output_dir: str = None) -> None:
    """
    Convert XMind file to Markdown format.
    
    Args:
        xmind_file_path: Path to the XMind file
        output_dir: Directory to save the output (defaults to current directory)
    """
    try:
        # Validate input file
        if not os.path.exists(xmind_file_path):
            raise FileNotFoundError(f"XMind file not found: {xmind_file_path}")
        
        if not xmind_file_path.endswith('.xmind'):
            raise ValueError("File must have .xmind extension")
        
        # Load and parse XMind map
        logger.info(f"Loading XMind file: {xmind_file_path}")
        xmind_map = XMindMapAccesser(xmind_file_path)
        logger.info("XMind Map loaded successfully")
        
        # Get map information
        map_levels = xmind_map.get_number_of_levels()
        logger.info(f"Number of levels in the XMind map: {map_levels}")
        
        # Generate markdown
        logger.info("Generating Markdown...")
        map_markdown = xmind_map.generate_markdown()
        
        # Determine output path
        base_name = os.path.splitext(os.path.basename(xmind_file_path))[0]
        if output_dir is None:
            output_dir = os.path.dirname(xmind_file_path) or '.'
        
        output_path = os.path.join(output_dir, f"{base_name}_output.md")
        
        # Save markdown file
        with open(output_path, "w", encoding='utf-8') as md_file:
            md_file.write(map_markdown)
        
        logger.info(f"Markdown saved successfully to: {output_path}")
        print(f"\n✓ Conversion complete! Output saved to:\n  {output_path}")
        
    except Exception as e:
        logger.error(f"Conversion failed: {e}", exc_info=True)
        raise


def convert_to_csv(xmind_file_path: str, output_dir: str = None) -> None:
    """
    Convert XMind file to CSV format.
    
    Args:
        xmind_file_path: Path to the XMind file
        output_dir: Directory to save the output (defaults to current directory)
    """
    try:
        # Validate input file
        if not os.path.exists(xmind_file_path):
            raise FileNotFoundError(f"XMind file not found: {xmind_file_path}")
        
        # Load and parse XMind map
        logger.info(f"Loading XMind file: {xmind_file_path}")
        xmind_map = XMindMapAccesser(xmind_file_path)
        
        # Generate DataFrame
        logger.info("Generating DataFrame...")
        df = xmind_map.get_dataframe()
        
        # Determine output path
        base_name = os.path.splitext(os.path.basename(xmind_file_path))[0]
        if output_dir is None:
            output_dir = os.path.dirname(xmind_file_path) or '.'
        
        output_path = os.path.join(output_dir, f"{base_name}_output.csv")
        
        # Save CSV file
        df.to_csv(output_path, index=False, encoding='utf-8')
        
        logger.info(f"CSV saved successfully to: {output_path}")
        print(f"\n✓ Conversion complete! Output saved to:\n  {output_path}")
        
    except Exception as e:
        logger.error(f"Conversion failed: {e}", exc_info=True)
        raise


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Convert XMind files to various formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py input.xmind --format markdown
  python main.py input.xmind --format csv --output ./outputs
  python main.py input.xmind -f markdown -o ~/Documents
        """
    )
    
    parser.add_argument(
        'input_file',
        help='Path to the XMind file to convert'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['markdown', 'csv'],
        default='markdown',
        help='Output format (default: markdown)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output directory (default: same as input file)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Convert based on format
    if args.format == 'markdown':
        convert_to_markdown(args.input_file, args.output)
    elif args.format == 'csv':
        convert_to_csv(args.input_file, args.output)


if __name__ == "__main__":
    main()
