#!/usr/bin/env python3
"""
XMind Converter - Unified Command Line Interface

Convert XMind mind maps to various formats:
- Markdown with wiki-style links
- CSV with hierarchical columns  
- Notion database pages
- Neo4j graph database
"""
import argparse
import sys
import logging
from pathlib import Path

from xmind_converter.core.parser import XMindParser
from xmind_converter.core.config import Config
from xmind_converter.converters import (
    MarkdownConverter,
    CSVConverter,
    NotionConverter,
    Neo4jConverter
)

logger = logging.getLogger(__name__)


def convert_markdown(args):
    """Convert to Markdown format."""
    parser = XMindParser(args.input)
    converter = MarkdownConverter(parser)
    output = converter.convert(output_dir=args.output)
    print(f"✓ Markdown saved to: {output}")


def convert_csv(args):
    """Convert to CSV format."""
    parser = XMindParser(args.input)
    converter = CSVConverter(parser)
    output = converter.convert(output_dir=args.output)
    print(f"✓ CSV saved to: {output}")


def convert_notion(args):
    """Convert to Notion database."""
    from notion_client import Client
    
    # Get credentials
    token = args.token
    db_id = args.database_id
    
    if not token or not db_id:
        token, db_id = Config.get_notion_credentials()
    
    if not token or not db_id:
        print("✗ Error: Notion credentials not found.")
        print("  Set NOTION_TOKEN and NOTION_DATABASE_ID environment variables,")
        print("  or use --token and --database-id options.")
        return 1
    
    # Convert
    parser = XMindParser(args.input)
    notion_client = Client(auth=token)
    converter = NotionConverter(parser, notion_client, db_id)
    result = converter.convert()
    print(f"✓ {result}")
    return 0


def convert_neo4j(args):
    """Convert to Neo4j graph database."""
    # Get credentials
    uri = args.uri
    username = args.username
    password = args.password
    
    if not all([uri, username, password]):
        uri, username, password = Config.get_neo4j_credentials()
    
    if not all([uri, username, password]):
        print("✗ Error: Neo4j credentials not found.")
        print("  Set NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD environment variables,")
        print("  or use --uri, --username, and --password options.")
        return 1
    
    # Convert
    parser = XMindParser(args.input)
    converter = Neo4jConverter(parser, uri, username, password)
    try:
        result = converter.convert(relationship_type=args.relationship)
        print(f"✓ {result}")
        return 0
    finally:
        converter.close()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='xmind-convert',
        description='Convert XMind mind maps to various formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert to Markdown
  xmind-convert input.xmind markdown
  xmind-convert input.xmind markdown --output ./docs
  
  # Convert to CSV
  xmind-convert input.xmind csv --output ./data
  
  # Convert to Notion (using environment variables)
  xmind-convert input.xmind notion
  
  # Convert to Notion (with explicit credentials)
  xmind-convert input.xmind notion --token secret_xyz --database-id abc123
  
  # Convert to Neo4j
  xmind-convert input.xmind neo4j --uri bolt://localhost:7687 --username neo4j --password pass
  
  # Convert with custom relationship type
  xmind-convert input.xmind neo4j --relationship CONTAINS

For more information, visit: https://github.com/MarlinZH/xmind_converter
        """
    )
    
    parser.add_argument(
        'input',
        help='Path to the XMind file to convert'
    )
    
    parser.add_argument(
        'format',
        choices=['markdown', 'csv', 'notion', 'neo4j'],
        help='Output format'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output directory (for file-based formats)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    # Notion options
    notion_group = parser.add_argument_group('Notion options')
    notion_group.add_argument(
        '--token',
        help='Notion API integration token'
    )
    notion_group.add_argument(
        '--database-id',
        help='Notion database ID'
    )
    
    # Neo4j options
    neo4j_group = parser.add_argument_group('Neo4j options')
    neo4j_group.add_argument(
        '--uri',
        help='Neo4j database URI (e.g., bolt://localhost:7687)'
    )
    neo4j_group.add_argument(
        '--username',
        help='Neo4j username'
    )
    neo4j_group.add_argument(
        '--password',
        help='Neo4j password'
    )
    neo4j_group.add_argument(
        '--relationship',
        default='HAS_CHILD',
        help='Relationship type for Neo4j edges (default: HAS_CHILD)'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = 'DEBUG' if args.verbose else 'INFO'
    Config.setup_logging(log_level)
    
    # Validate input file
    if not Path(args.input).exists():
        print(f"✗ Error: File not found: {args.input}")
        return 1
    
    try:
        # Route to appropriate converter
        if args.format == 'markdown':
            convert_markdown(args)
        elif args.format == 'csv':
            convert_csv(args)
        elif args.format == 'notion':
            return convert_notion(args)
        elif args.format == 'neo4j':
            return convert_neo4j(args)
        
        return 0
        
    except Exception as e:
        logger.error(f"Conversion failed: {e}", exc_info=args.verbose)
        print(f"✗ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
