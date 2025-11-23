#!/usr/bin/env python3
"""
Sample Data Generator for RAG Chatbot Demo

This script generates synthetic data for the RAG chatbot demo based on configuration.
It supports multiple domains (tech, healthcare, finance, ecommerce) and can generate
various volumes and complexity levels of data.

Usage:
    python generate_sample_data.py

Configuration:
    - Edit data-generators/config.yaml to change settings
    - Or set environment variables (see env.example)
"""

import os
import yaml
import random
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv

class DataGenerator:
    """Main data generator class"""
    
    def __init__(self):
        # Configuration can come from YAML, .env, or environment variables.
        # This mirrors the typical workflow students will encounter in production.
        self.config = self._load_config()
        self._setup_random_seed()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file and environment variables"""
        config_path = Path(__file__).parent / "config.yaml"
        
        # Load YAML config
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
        else:
            config = self._get_default_config()
            
        # Override with environment variables if present
        env_file = Path(__file__).parent / ".env"
        if env_file.exists():
            load_dotenv(env_file)
        
        # Override config with env vars
        env_overrides = {
            "DATA_DOMAIN": ("data_generation", "domain"),
            "DATA_VOLUME": ("data_generation", "volume"),
            "DATA_COMPLEXITY": ("data_generation", "complexity"),
            "OUTPUT_DIR": ("data_generation", "output_dir"),
            "OVERWRITE_EXISTING": ("data_generation", "overwrite_existing"),
            "DATA_LANGUAGE": ("data_generation", "language"),
            "INCLUDE_EXAMPLES": ("data_generation", "include_examples"),
            "INCLUDE_TROUBLESHOOTING": ("data_generation", "include_troubleshooting"),
        }
        
        for env_var, (section, key) in env_overrides.items():
            value = os.getenv(env_var)
            if value is not None:
                # Convert string values to appropriate types
                if key in ["overwrite_existing", "include_examples", "include_troubleshooting"]:
                    value = value.lower() in ("true", "1", "yes")
                config[section][key] = value
                
        return config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "data_generation": {
                "domain": "tech",
                "volume": "medium",
                "complexity": "intermediate",
                "output_dir": "../backend/data",
                "overwrite_existing": False,
                "language": "en",
                "include_examples": True,
                "include_troubleshooting": True
            },
            "data_structure": {
                "docs": {"enabled": True, "chunk_size": 1000, "chunk_overlap": 200},
                "tickets": {"enabled": True, "severity_levels": ["low", "medium", "high"]},
                "configs": {"enabled": True, "formats": ["yaml", "json"]},
                "chat_history": {"enabled": True, "conversation_length": "medium"}
            }
        }
    
    def _setup_random_seed(self):
        """Setup random seed for reproducible results"""
        seed = self.config.get("generation", {}).get("seed")
        if seed is not None:
            random.seed(seed)
    
    def generate_all(self):
        """Generate all data types based on configuration"""
        domain = self.config["data_generation"]["domain"]
        volume = self.config["data_generation"]["volume"]
        output_dir = Path(self.config["data_generation"]["output_dir"])
        
        print(f"Generating {volume} {domain} data...")
        print(f" Output directory: {output_dir.absolute()}")
        
        # Create output directories
        self._create_output_dirs(output_dir)
        
        # Generate data based on domain
        # Each domain module exposes the same interface so swapping domains stays simple.
        if domain == "tech":
            self._generate_tech_data(output_dir, volume)
        elif domain == "healthcare":
            self._generate_healthcare_data(output_dir, volume)
        elif domain == "finance":
            self._generate_finance_data(output_dir, volume)
        elif domain == "ecommerce":
            self._generate_ecommerce_data(output_dir, volume)
        else:
            self._generate_general_data(output_dir, volume)
            
        print(f" Generated {domain} data in {output_dir}")
    
    def _create_output_dirs(self, output_dir: Path):
        """Create necessary output directories"""
        dirs = ["docs", "tickets", "configs", "chat_history"]
        for dir_name in dirs:
            dir_path = output_dir / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f" Created directory: {dir_path}")
    
    def _generate_tech_data(self, output_dir: Path, volume: str):
        """Generate tech domain data"""
        try:
            from domains.tech import TechDataGenerator
            generator = TechDataGenerator(self.config)
            generator.generate_docs(output_dir / "docs", volume)
            generator.generate_tickets(output_dir / "tickets", volume)
            generator.generate_configs(output_dir / "configs", volume)
            generator.generate_chat_history(output_dir / "chat_history", volume)
        except ImportError:
            print("  Tech domain generator not found, using fallback")
            self._generate_fallback_data(output_dir, volume, "tech")
    
    def _generate_healthcare_data(self, output_dir: Path, volume: str):
        """Generate healthcare domain data"""
        try:
            from domains.healthcare import HealthcareDataGenerator
            generator = HealthcareDataGenerator(self.config)
            generator.generate_docs(output_dir / "docs", volume)
            generator.generate_tickets(output_dir / "tickets", volume)
            generator.generate_configs(output_dir / "configs", volume)
            generator.generate_chat_history(output_dir / "chat_history", volume)
        except ImportError:
            print("  Healthcare domain generator not found, using fallback")
            self._generate_fallback_data(output_dir, volume, "healthcare")
    
    def _generate_finance_data(self, output_dir: Path, volume: str):
        """Generate finance domain data"""
        try:
            from domains.finance import FinanceDataGenerator
            generator = FinanceDataGenerator(self.config)
            generator.generate_docs(output_dir / "docs", volume)
            generator.generate_tickets(output_dir / "tickets", volume)
            generator.generate_configs(output_dir / "configs", volume)
            generator.generate_chat_history(output_dir / "chat_history", volume)
        except ImportError:
            print("  Finance domain generator not found, using fallback")
            self._generate_fallback_data(output_dir, volume, "finance")
    
    def _generate_ecommerce_data(self, output_dir: Path, volume: str):
        """Generate ecommerce domain data"""
        try:
            from domains.ecommerce import EcommerceDataGenerator
            generator = EcommerceDataGenerator(self.config)
            generator.generate_docs(output_dir / "docs", volume)
            generator.generate_tickets(output_dir / "tickets", volume)
            generator.generate_configs(output_dir / "configs", volume)
            generator.generate_chat_history(output_dir / "chat_history", volume)
        except ImportError:
            print("  Ecommerce domain generator not found, using fallback")
            self._generate_fallback_data(output_dir, volume, "ecommerce")
    
    def _generate_general_data(self, output_dir: Path, volume: str):
        """Generate general domain data"""
        self._generate_fallback_data(output_dir, volume, "general")
    
    def _generate_fallback_data(self, output_dir: Path, volume: str, domain: str):
        """Generate basic fallback data when domain generators are not available"""
        print(f" Generating basic {domain} data...")
        
        # Determine number of items based on volume
        item_counts = {"small": 5, "medium": 15, "large": 30}
        count = item_counts.get(volume, 15)
        
        # Generate basic docs
        docs = [
            f"# {domain.title()} Documentation\n\nThis is sample documentation for {domain} domain.",
            f"# Getting Started with {domain.title()}\n\nBasic setup and configuration guide.",
            f"# Troubleshooting {domain.title()}\n\nCommon issues and solutions.",
            f"# Advanced {domain.title()}\n\nAdvanced features and configurations.",
            f"# API Reference for {domain.title()}\n\nComplete API documentation."
        ]
        
        for i, doc in enumerate(docs[:count]):
            (output_dir / "docs" / f"doc_{i+1}.md").write_text(doc)
        
        # Generate basic tickets
        tickets = [
            f"User reports issue with {domain} system",
            f"Configuration error in {domain} setup",
            f"Performance issue with {domain} application",
            f"Authentication problem in {domain} service",
            f"Database connection issue in {domain}"
        ]
        
        for i, ticket in enumerate(tickets[:count]):
            (output_dir / "tickets" / f"ticket_{i+1}.txt").write_text(ticket)
        
        # Generate basic configs
        configs = [
            f"# {domain.title()} Configuration\nsetting1: value1\nsetting2: value2",
            f"# {domain.title()} Settings\noption1: enabled\noption2: disabled",
            f"# {domain.title()} Config\nfeature1: true\nfeature2: false"
        ]
        
        for i, config in enumerate(configs[:count]):
            (output_dir / "configs" / f"config_{i+1}.yaml").write_text(config)
        
        # Generate basic chat history
        chat_history = [
            f"user: How do I configure {domain}?",
            f"assistant: You can configure {domain} by editing the config file.",
            f"user: What are the main features?",
            f"assistant: The main features include setup, configuration, and monitoring.",
            f"user: How do I troubleshoot issues?",
            f"assistant: Check the logs and documentation for troubleshooting steps."
        ]
        
        for i, chat in enumerate(chat_history[:count]):
            (output_dir / "chat_history" / f"chat_{i+1}.txt").write_text(chat)

def main():
    """Main entry point"""
    try:
        generator = DataGenerator()
        generator.generate_all()
    except Exception as e:
        print(f"Error generating data: {e}")
        print(" Make sure you have the required dependencies installed:")
        print("   pip install pyyaml python-dotenv")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())
