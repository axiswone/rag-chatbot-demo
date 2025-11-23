"""
Ecommerce Domain Data Generator

Generates synthetic data for ecommerce-focused RAG chatbot demo.
Includes inventory management, order processing, customer service, and ecommerce chat history.
"""

from faker import Faker
from pathlib import Path
from typing import List, Dict, Any
import random
import json

class EcommerceDataGenerator:
    """Generator for ecommerce domain data"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.fake = Faker()
        self.domain_config = config["data_generation"].get("ecommerce", {})
        self.focus_areas = self.domain_config.get("focus_areas", ["inventory", "orders", "payments", "customer_service"])
        self.platforms = self.domain_config.get("platforms", ["shopify", "woocommerce", "custom"])
        self.business_models = self.domain_config.get("business_models", ["b2c", "b2b", "marketplace"])
        
    def generate_docs(self, output_dir: Path, volume: str):
        """Generate ecommerce documentation"""
        print(f" Generating {volume} ecommerce documentation...")
        
        docs = []
        
        if volume == "small":
            docs = self._generate_small_docs()
        elif volume == "medium":
            docs = self._generate_medium_docs()
        else:  # large
            docs = self._generate_large_docs()
        
        # Write to files
        for i, doc in enumerate(docs):
            (output_dir / f"ecommerce_doc_{i+1}.md").write_text(doc)
        
        print(f" Generated {len(docs)} documentation files")
    
    def _generate_small_docs(self) -> List[str]:
        """Generate small set of ecommerce docs"""
        return [
            f"# {self.focus_areas[0].title()} Management\n\n"
            f"Comprehensive inventory management system:\n\n"
            f"## Key Features\n- Real-time stock tracking\n- Automated reorder points\n- Multi-location support\n- Product variants\n\n"
            f"## Inventory Operations\n- Stock adjustments\n- Transfer between locations\n- Cycle counting\n- Dead stock management\n\n"
            f"## Integration\n- {self.platforms[0].title()} integration\n- Supplier systems\n- Analytics platforms\n- Reporting tools",
            
            f"# {self.focus_areas[1].title()} Processing\n\n"
            f"Order processing and fulfillment system:\n\n"
            f"## Order Lifecycle\n- Order placement\n- Payment processing\n- Inventory allocation\n- Fulfillment\n- Shipping\n- Delivery confirmation\n\n"
            f"## Order Management\n- Order status tracking\n- Modification requests\n- Cancellation handling\n- Refund processing\n\n"
            f"## Fulfillment\n- Pick and pack operations\n- Shipping label generation\n- Carrier integration\n- Delivery tracking",
            
            f"# {self.focus_areas[2].title()} Integration\n\n"
            f"Payment processing and gateway integration:\n\n"
            f"## Payment Methods\n- Credit/Debit cards\n- Digital wallets\n- Bank transfers\n- Buy now, pay later\n\n"
            f"## Security\n- PCI DSS compliance\n- Tokenization\n- Fraud detection\n- Secure checkout\n\n"
            f"## Processing\n- Real-time processing\n- Batch processing\n- Reconciliation\n- Chargeback handling"
        ]
    
    def _generate_medium_docs(self) -> List[str]:
        """Generate medium set of ecommerce docs"""
        docs = self._generate_small_docs()
        
        # Add more comprehensive docs
        docs.extend([
            f"# Customer Service Platform\n\n"
            f"Comprehensive customer service and support system:\n\n"
            f"## Support Channels\n- Live chat\n- Email support\n- Phone support\n- Social media\n- Self-service portal\n\n"
            f"## Ticket Management\n- Issue categorization\n- Priority assignment\n- Escalation procedures\n- Resolution tracking\n\n"
            f"## Knowledge Base\n- FAQ management\n- Product guides\n- Troubleshooting\n- Video tutorials",
            
            f"# Analytics and Reporting\n\n"
            f"Ecommerce analytics and business intelligence:\n\n"
            f"## Key Metrics\n- Sales performance\n- Customer behavior\n- Product performance\n- Marketing effectiveness\n\n"
            f"## Reporting\n- Real-time dashboards\n- Scheduled reports\n- Custom analytics\n- Data export\n\n"
            f"## Insights\n- Trend analysis\n- Predictive analytics\n- Customer segmentation\n- Performance optimization",
            
            f"# Marketing Automation\n\n"
            f"Marketing automation and customer engagement:\n\n"
            f"## Email Marketing\n- Automated campaigns\n- Personalization\n- A/B testing\n- Performance tracking\n\n"
            f"## Customer Engagement\n- Loyalty programs\n- Referral systems\n- Reviews and ratings\n- Social media integration\n\n"
            f"## Conversion Optimization\n- Cart abandonment recovery\n- Product recommendations\n- Upselling strategies\n- Cross-selling tactics"
        ])
        
        return docs
    
    def _generate_large_docs(self) -> List[str]:
        """Generate large set of ecommerce docs"""
        docs = self._generate_medium_docs()
        
        # Add extensive documentation
        for platform in self.platforms:
            docs.append(f"# {platform.title()} Platform Integration\n\n"
                       f"Integration guide for {platform.title()} platform:\n\n"
                       f"## Setup and Configuration\n- Platform installation\n- Theme customization\n- Plugin configuration\n- API integration\n\n"
                       f"## Features and Functionality\n- Product management\n- Order processing\n- Customer management\n- Analytics integration\n\n"
                       f"## Best Practices\n- Performance optimization\n- Security considerations\n- SEO optimization\n- Mobile responsiveness")
        
        # Add business model documentation
        for model in self.business_models:
            docs.append(f"# {model.upper()} Business Model\n\n"
                       f"Comprehensive guide for {model.upper()} ecommerce:\n\n"
                       f"## Business Strategy\n- Target market analysis\n- Competitive positioning\n- Revenue models\n- Growth strategies\n\n"
                       f"## Operational Requirements\n- Infrastructure needs\n- Staff requirements\n- Technology stack\n- Compliance requirements\n\n"
                       f"## Success Metrics\n- Key performance indicators\n- Financial metrics\n- Customer metrics\n- Operational metrics")
        
        return docs
    
    def generate_tickets(self, output_dir: Path, volume: str):
        """Generate ecommerce support tickets"""
        print(f" Generating {volume} ecommerce support tickets...")
        
        tickets = []
        
        if volume == "small":
            tickets = self._generate_small_tickets()
        elif volume == "medium":
            tickets = self._generate_medium_tickets()
        else:  # large
            tickets = self._generate_large_tickets()
        
        # Write to files
        for i, ticket in enumerate(tickets):
            (output_dir / f"ecommerce_ticket_{i+1}.json").write_text(json.dumps(ticket, indent=2))
        
        print(f" Generated {len(tickets)} support tickets")
    
    def _generate_small_tickets(self) -> List[Dict[str, Any]]:
        """Generate small set of ecommerce tickets"""
        return [
            {
                "id": f"ECO-{self.fake.random_int(min=1000, max=9999)}",
                "title": "Order processing delay",
                "description": "Customer order #12345 has been pending for 24 hours. Payment was processed but order status remains 'processing'.",
                "severity": "high",
                "status": "open",
                "priority": "p1",
                "reporter": "Customer Service",
                "assignee": "order-team",
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": ["order", "processing", "delay"],
                "platform": random.choice(self.platforms)
            },
            {
                "id": f"ECO-{self.fake.random_int(min=1000, max=9999)}",
                "title": "Inventory sync issue",
                "description": "Product inventory levels not syncing between {self.platforms[0]} and warehouse management system.",
                "severity": "medium",
                "status": "in_progress",
                "priority": "p2",
                "reporter": "Inventory Manager",
                "assignee": "tech-team",
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": ["inventory", "sync", "integration"],
                "platform": random.choice(self.platforms)
            },
            {
                "id": f"ECO-{self.fake.random_int(min=1000, max=9999)}",
                "title": "Payment gateway error",
                "description": "Customers reporting payment failures at checkout. Error code: PAYMENT_GATEWAY_TIMEOUT",
                "severity": "critical",
                "status": "open",
                "priority": "p1",
                "reporter": "Customer Service",
                "assignee": "payment-team",
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": ["payment", "gateway", "checkout"],
                "platform": random.choice(self.platforms)
            }
        ]
    
    def _generate_medium_tickets(self) -> List[Dict[str, Any]]:
        """Generate medium set of ecommerce tickets"""
        tickets = self._generate_small_tickets()
        
        # Add more tickets
        for i in range(5):
            tickets.append({
                "id": f"ECO-{self.fake.random_int(min=1000, max=9999)}",
                "title": f"{self.fake.sentence(nb_words=4)}",
                "description": f"Ecommerce issue reported: {self.fake.text(max_nb_chars=200)}",
                "severity": random.choice(["low", "medium", "high", "critical"]),
                "status": random.choice(["open", "in_progress", "resolved"]),
                "priority": f"p{random.randint(1, 4)}",
                "reporter": random.choice(["Customer Service", "Inventory Manager", "Marketing Team", "IT Support"]),
                "assignee": random.choice(["order-team", "tech-team", "payment-team", "customer-service"]),
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": [random.choice(self.focus_areas), random.choice(self.business_models)],
                "platform": random.choice(self.platforms)
            })
        
        return tickets
    
    def _generate_large_tickets(self) -> List[Dict[str, Any]]:
        """Generate large set of ecommerce tickets"""
        tickets = self._generate_medium_tickets()
        
        # Add many more tickets
        for i in range(20):
            tickets.append({
                "id": f"ECO-{self.fake.random_int(min=1000, max=9999)}",
                "title": f"{self.fake.sentence(nb_words=5)}",
                "description": f"Detailed ecommerce issue: {self.fake.text(max_nb_chars=300)}",
                "severity": random.choice(["low", "medium", "high", "critical"]),
                "status": random.choice(["open", "in_progress", "resolved", "closed"]),
                "priority": f"p{random.randint(1, 4)}",
                "reporter": random.choice(["Customer Service", "Inventory Manager", "Marketing Team", "IT Support", "Operations"]),
                "assignee": random.choice(["order-team", "tech-team", "payment-team", "customer-service", "marketing-team"]),
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": [random.choice(self.focus_areas), random.choice(self.business_models), random.choice(self.platforms)],
                "platform": random.choice(self.platforms)
            })
        
        return tickets
    
    def generate_configs(self, output_dir: Path, volume: str):
        """Generate ecommerce configuration files"""
        print(f"  Generating {volume} ecommerce configuration files...")
        
        configs = []
        
        if volume == "small":
            configs = self._generate_small_configs()
        elif volume == "medium":
            configs = self._generate_medium_configs()
        else:  # large
            configs = self._generate_large_configs()
        
        # Write to files
        for i, config in enumerate(configs):
            (output_dir / f"ecommerce_config_{i+1}.yaml").write_text(config)
        
        print(f" Generated {len(configs)} configuration files")
    
    def _generate_small_configs(self) -> List[str]:
        """Generate small set of ecommerce configs"""
        return [
            f"# Ecommerce Platform Configuration\n"
            f"platform:\n"
            f"  name: \"{self.platforms[0].title()}\"\n"
            f"  version: \"2.1.0\"\n"
            f"  theme: \"modern\"\n"
            f"  currency: \"USD\"\n"
            f"  timezone: \"America/New_York\"\n"
            f"  language: \"en\"\n"
            f"  features:\n"
            f"    - product_catalog\n"
            f"    - shopping_cart\n"
            f"    - checkout_process\n"
            f"    - order_management",
            
            f"# Inventory Management Settings\n"
            f"inventory:\n"
            f"  tracking_enabled: true\n"
            f"  low_stock_threshold: 10\n"
            f"  reorder_point: 5\n"
            f"  locations:\n"
            f"    - warehouse_main\n"
            f"    - warehouse_secondary\n"
            f"    - store_front\n"
            f"  sync_frequency: 15_minutes\n"
            f"  alerts:\n"
            f"    email: inventory@company.com\n"
            f"    slack: #inventory-alerts",
            
            f"# Order Processing Configuration\n"
            f"orders:\n"
            f"  auto_fulfillment: true\n"
            f"  fulfillment_time: 24_hours\n"
            f"  shipping_methods:\n"
            f"    - standard\n"
            f"    - express\n"
            f"    - overnight\n"
            f"  carriers:\n"
            f"    - ups\n"
            f"    - fedex\n"
            f"    - usps\n"
            f"  tracking:\n"
            f"    enabled: true\n"
            f"    notifications: true"
        ]
    
    def _generate_medium_configs(self) -> List[str]:
        """Generate medium set of ecommerce configs"""
        configs = self._generate_small_configs()
        
        # Add more configs
        configs.extend([
            f"# Payment Gateway Integration\n"
            f"payment_gateway:\n"
            f"  provider: \"Stripe\"\n"
            f"  api_key: \"sk_test_...\"\n"
            f"  webhook_secret: \"whsec_...\"\n"
            f"  methods:\n"
            f"    - credit_card\n"
            f"    - debit_card\n"
            f"    - paypal\n"
            f"    - apple_pay\n"
            f"    - google_pay\n"
            f"  security:\n"
            f"    pci_compliant: true\n"
            f"    tokenization: true\n"
            f"    fraud_detection: true",
            
            f"# Customer Service Settings\n"
            f"customer_service:\n"
            f"  channels:\n"
            f"    - live_chat\n"
            f"    - email\n"
            f"    - phone\n"
            f"    - social_media\n"
            f"  hours:\n"
            f"    monday_friday: \"9:00-18:00\"\n"
            f"    saturday: \"10:00-16:00\"\n"
            f"    sunday: \"closed\"\n"
            f"  escalation:\n"
            f"    level_1: customer_service\n"
            f"    level_2: supervisor\n"
            f"    level_3: manager"
        ])
        
        return configs
    
    def _generate_large_configs(self) -> List[str]:
        """Generate large set of ecommerce configs"""
        configs = self._generate_medium_configs()
        
        # Add extensive configs
        for platform in self.platforms:
            configs.append(f"# {platform.title()} Platform Settings\n"
                         f"{platform.lower()}:\n"
                         f"  platform_id: {platform.upper()}_001\n"
                         f"  admin_user: admin@{platform}.com\n"
                         f"  api_version: v1\n"
                         f"  webhook_url: https://api.company.com/webhooks/{platform}\n"
                         f"  features:\n"
                         f"    - product_management\n"
                         f"    - order_processing\n"
                         f"    - customer_management\n"
                         f"    - analytics\n"
                         f"  limits:\n"
                         f"    max_products: {random.randint(1000, 10000)}\n"
                         f"    max_orders_per_day: {random.randint(100, 1000)}\n"
                         f"    storage_limit: {random.randint(1, 10)}GB")
        
        return configs
    
    def generate_chat_history(self, output_dir: Path, volume: str):
        """Generate ecommerce chat history"""
        print(f" Generating {volume} ecommerce chat history...")
        
        conversations = []
        
        if volume == "small":
            conversations = self._generate_small_conversations()
        elif volume == "medium":
            conversations = self._generate_medium_conversations()
        else:  # large
            conversations = self._generate_large_conversations()
        
        # Write to files
        for i, conversation in enumerate(conversations):
            (output_dir / f"ecommerce_chat_{i+1}.json").write_text(json.dumps(conversation, indent=2))
        
        print(f" Generated {len(conversations)} chat conversations")
    
    def _generate_small_conversations(self) -> List[Dict[str, Any]]:
        """Generate small set of ecommerce conversations"""
        return [
            {
                "user_id": "customer_service_rep",
                "session_id": self.fake.uuid4(),
                "messages": [
                    {"role": "user", "message": "Customer can't complete checkout, what should I do?"},
                    {"role": "assistant", "message": "For checkout issues, check:\n1. Payment method validity\n2. Shipping address\n3. Cart contents\n4. Browser compatibility\n\nCommon solutions include clearing cache, trying different payment method, or contacting payment support."},
                    {"role": "user", "message": "What about inventory issues?"},
                    {"role": "assistant", "message": "For inventory problems:\n1. Check stock levels\n2. Verify product availability\n3. Check for sync issues\n4. Update customer on expected restock\n\nAlways provide accurate information about product availability."}
                ],
                "timestamp": self.fake.date_time_this_month().isoformat(),
                "platform": random.choice(self.platforms)
            },
            {
                "user_id": "inventory_manager",
                "session_id": self.fake.uuid4(),
                "messages": [
                    {"role": "user", "message": "How do I sync inventory between systems?"},
                    {"role": "assistant", "message": "Inventory sync can be done through:\n1. API integration\n2. Scheduled batch updates\n3. Real-time webhooks\n4. Manual reconciliation\n\nEnsure all systems are configured with the same product SKUs and locations."},
                    {"role": "user", "message": "What about low stock alerts?"},
                    {"role": "assistant", "message": "Low stock alerts can be configured to:\n1. Notify via email/Slack\n2. Auto-reorder products\n3. Hide out-of-stock items\n4. Show expected restock dates\n\nSet appropriate thresholds based on sales velocity and lead times."}
                ],
                "timestamp": self.fake.date_time_this_month().isoformat(),
                "platform": random.choice(self.platforms)
            }
        ]
    
    def _generate_medium_conversations(self) -> List[Dict[str, Any]]:
        """Generate medium set of ecommerce conversations"""
        conversations = self._generate_small_conversations()
        
        # Add more conversations
        for i in range(3):
            conversations.append({
                "user_id": f"ecommerce_user_{i+1}",
                "session_id": self.fake.uuid4(),
                "messages": [
                    {"role": "user", "message": f"How do I set up {random.choice(self.focus_areas)}?"},
                    {"role": "assistant", "message": f"Setting up {random.choice(self.focus_areas)} involves several steps. Let me guide you through the process."},
                    {"role": "user", "message": "What are the best practices?"},
                    {"role": "assistant", "message": f"Best practices include regular monitoring, automation where possible, and maintaining data accuracy."},
                    {"role": "user", "message": "Thanks for the help!"},
                    {"role": "assistant", "message": "You're welcome! Feel free to ask if you need any clarification."}
                ],
                "timestamp": self.fake.date_time_this_month().isoformat(),
                "platform": random.choice(self.platforms)
            })
        
        return conversations
    
    def _generate_large_conversations(self) -> List[Dict[str, Any]]:
        """Generate large set of ecommerce conversations"""
        conversations = self._generate_medium_conversations()
        
        # Add many more conversations
        for i in range(10):
            conversations.append({
                "user_id": f"ecommerce_user_{i+10}",
                "session_id": self.fake.uuid4(),
                "messages": [
                    {"role": "user", "message": f"I need help with {random.choice(self.focus_areas)}"},
                    {"role": "assistant", "message": f"I'd be happy to help you with {random.choice(self.focus_areas)}. What specific issue are you facing?"},
                    {"role": "user", "message": f"The system is showing {random.choice(self.platforms)} integration error"},
                    {"role": "assistant", "message": f"For {random.choice(self.platforms)} integration issues, here are some steps:\n1. Check API credentials\n2. Verify webhook configuration\n3. Test connection\n4. Contact support if needed"},
                    {"role": "user", "message": "Can you provide more specific guidance?"},
                    {"role": "assistant", "message": f"Certainly! For {random.choice(self.focus_areas)} issues, you should:\n- Check the documentation\n- Review system logs\n- Test with minimal setup\n- Contact support if needed"}
                ],
                "timestamp": self.fake.date_time_this_month().isoformat(),
                "platform": random.choice(self.platforms)
            })
        
        return conversations
