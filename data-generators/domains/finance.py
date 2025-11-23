"""
Finance Domain Data Generator

Generates synthetic data for finance-focused RAG chatbot demo.
Includes payment processing, risk management, compliance, and financial chat history.
"""

from faker import Faker
from pathlib import Path
from typing import List, Dict, Any
import random
import json

class FinanceDataGenerator:
    """Generator for finance domain data"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.fake = Faker()
        self.domain_config = config["data_generation"].get("finance", {})
        self.focus_areas = self.domain_config.get("focus_areas", ["payments", "risk_management", "compliance"])
        self.products = self.domain_config.get("products", ["banking", "investment", "insurance"])
        self.regulations = self.domain_config.get("regulations", ["pci_dss", "sox", "basel_iii"])
        
    def generate_docs(self, output_dir: Path, volume: str):
        """Generate finance documentation"""
        print(f" Generating {volume} finance documentation...")
        
        docs = []
        
        if volume == "small":
            docs = self._generate_small_docs()
        elif volume == "medium":
            docs = self._generate_medium_docs()
        else:  # large
            docs = self._generate_large_docs()
        
        # Write to files
        for i, doc in enumerate(docs):
            (output_dir / f"finance_doc_{i+1}.md").write_text(doc)
        
        print(f" Generated {len(docs)} documentation files")
    
    def _generate_small_docs(self) -> List[str]:
        """Generate small set of finance docs"""
        return [
            f"# {self.focus_areas[0].title()} Processing\n\n"
            f"Payment processing system requirements and implementation:\n\n"
            f"## Key Features\n- Secure transaction processing\n- Multiple payment methods\n- Real-time fraud detection\n- Compliance with {self.regulations[0].upper()}\n\n"
            f"## Security Requirements\n- End-to-end encryption\n- Tokenization of sensitive data\n- PCI DSS compliance\n- Regular security audits\n\n"
            f"## Integration\n- API endpoints for payment processing\n- Webhook notifications\n- Reporting and analytics\n- Reconciliation processes",
            
            f"# {self.focus_areas[1].title()} Framework\n\n"
            f"Risk management framework for financial services:\n\n"
            f"## Risk Categories\n- Credit risk\n- Market risk\n- Operational risk\n- Liquidity risk\n\n"
            f"## Risk Assessment\n- Risk identification\n- Risk measurement\n- Risk monitoring\n- Risk reporting\n\n"
            f"## Mitigation Strategies\n- Diversification\n- Hedging\n- Insurance\n- Contingency planning",
            
            f"# {self.regulations[0].upper()} Compliance\n\n"
            f"Compliance requirements for {self.regulations[0].upper()}:\n\n"
            f"## Requirements\n- Data security standards\n- Access controls\n- Network security\n- Regular monitoring\n\n"
            f"## Implementation\n- Security policies\n- Technical controls\n- Administrative procedures\n- Incident response\n\n"
            f"## Auditing\n- Regular assessments\n- Vulnerability scanning\n- Penetration testing\n- Compliance reporting"
        ]
    
    def _generate_medium_docs(self) -> List[str]:
        """Generate medium set of finance docs"""
        docs = self._generate_small_docs()
        
        # Add more comprehensive docs
        docs.extend([
            f"# Fraud Detection System\n\n"
            f"Advanced fraud detection and prevention system:\n\n"
            f"## Detection Methods\n- Machine learning models\n- Rule-based systems\n- Behavioral analysis\n- Transaction monitoring\n\n"
            f"## Risk Scoring\n- Real-time risk assessment\n- Historical pattern analysis\n- Geographic risk factors\n- Device fingerprinting\n\n"
            f"## Response Actions\n- Automatic blocking\n- Manual review\n- Customer notification\n- Investigation procedures",
            
            f"# Investment Management Platform\n\n"
            f"Comprehensive investment management platform:\n\n"
            f"## Portfolio Management\n- Asset allocation\n- Risk assessment\n- Performance tracking\n- Rebalancing strategies\n\n"
            f"## Trading Features\n- Order management\n- Execution algorithms\n- Market data integration\n- Settlement processing\n\n"
            f"## Compliance\n- Regulatory reporting\n- Best execution\n- Client suitability\n- Record keeping",
            
            f"# Banking Operations\n\n"
            f"Core banking operations and processes:\n\n"
            f"## Account Management\n- Account opening\n- KYC procedures\n- Account maintenance\n- Account closure\n\n"
            f"## Transaction Processing\n- Deposit processing\n- Withdrawal processing\n- Transfer services\n- Check processing\n\n"
            f"## Customer Service\n- Support channels\n- Issue resolution\n- Product information\n- Complaint handling"
        ])
        
        return docs
    
    def _generate_large_docs(self) -> List[str]:
        """Generate large set of finance docs"""
        docs = self._generate_medium_docs()
        
        # Add extensive documentation
        for product in self.products:
            docs.append(f"# {product.title()} Services\n\n"
                       f"Comprehensive guide to {product} services:\n\n"
                       f"## Service Offerings\n- Core services\n- Premium services\n- Specialized products\n- Custom solutions\n\n"
                       f"## Operational Procedures\n- Service delivery\n- Quality assurance\n- Performance monitoring\n- Continuous improvement\n\n"
                       f"## Risk Management\n- Risk identification\n- Risk assessment\n- Risk mitigation\n- Risk monitoring")
        
        # Add regulatory documentation
        for regulation in self.regulations:
            docs.append(f"# {regulation.upper()} Compliance Framework\n\n"
                       f"Comprehensive compliance framework for {regulation.upper()}:\n\n"
                       f"## Regulatory Requirements\n- Mandatory requirements\n- Implementation guidelines\n- Monitoring procedures\n- Reporting obligations\n\n"
                       f"## Risk Management\n- Risk assessment\n- Mitigation strategies\n- Monitoring and review\n- Continuous improvement\n\n"
                       f"## Training and Education\n- Staff training programs\n- Competency assessment\n- Ongoing education\n- Certification requirements")
        
        return docs
    
    def generate_tickets(self, output_dir: Path, volume: str):
        """Generate finance support tickets"""
        print(f" Generating {volume} finance support tickets...")
        
        tickets = []
        
        if volume == "small":
            tickets = self._generate_small_tickets()
        elif volume == "medium":
            tickets = self._generate_medium_tickets()
        else:  # large
            tickets = self._generate_large_tickets()
        
        # Write to files
        for i, ticket in enumerate(tickets):
            (output_dir / f"finance_ticket_{i+1}.json").write_text(json.dumps(ticket, indent=2))
        
        print(f" Generated {len(tickets)} support tickets")
    
    def _generate_small_tickets(self) -> List[Dict[str, Any]]:
        """Generate small set of finance tickets"""
        return [
            {
                "id": f"FIN-{self.fake.random_int(min=1000, max=9999)}",
                "title": "Payment processing failure",
                "description": "Customer reports payment transaction failed with error code 5001. Transaction amount: $150.00",
                "severity": "high",
                "status": "open",
                "priority": "p1",
                "reporter": "Customer Service",
                "assignee": "payment-team",
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": ["payment", "transaction", "error"],
                "product": random.choice(self.products)
            },
            {
                "id": f"FIN-{self.fake.random_int(min=1000, max=9999)}",
                "title": "Fraud detection alert",
                "description": "System flagged suspicious transaction pattern. Multiple high-value transactions from same IP address.",
                "severity": "critical",
                "status": "in_progress",
                "priority": "p1",
                "reporter": "Fraud Detection System",
                "assignee": "fraud-team",
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": ["fraud", "security", "monitoring"],
                "product": random.choice(self.products)
            },
            {
                "id": f"FIN-{self.fake.random_int(min=1000, max=9999)}",
                "title": "Compliance reporting issue",
                "description": "Monthly compliance report generation failed. Error in data aggregation process.",
                "severity": "medium",
                "status": "open",
                "priority": "p2",
                "reporter": "Compliance Team",
                "assignee": "compliance-team",
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": ["compliance", "reporting", "data"],
                "product": random.choice(self.products)
            }
        ]
    
    def _generate_medium_tickets(self) -> List[Dict[str, Any]]:
        """Generate medium set of finance tickets"""
        tickets = self._generate_small_tickets()
        
        # Add more tickets
        for i in range(5):
            tickets.append({
                "id": f"FIN-{self.fake.random_int(min=1000, max=9999)}",
                "title": f"{self.fake.sentence(nb_words=4)}",
                "description": f"Finance issue reported: {self.fake.text(max_nb_chars=200)}",
                "severity": random.choice(["low", "medium", "high", "critical"]),
                "status": random.choice(["open", "in_progress", "resolved"]),
                "priority": f"p{random.randint(1, 4)}",
                "reporter": random.choice(["Customer Service", "Risk Team", "Compliance Team", "IT Support"]),
                "assignee": random.choice(["payment-team", "fraud-team", "compliance-team", "risk-team"]),
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": [random.choice(self.focus_areas), random.choice(self.regulations)],
                "product": random.choice(self.products)
            })
        
        return tickets
    
    def _generate_large_tickets(self) -> List[Dict[str, Any]]:
        """Generate large set of finance tickets"""
        tickets = self._generate_medium_tickets()
        
        # Add many more tickets
        for i in range(20):
            tickets.append({
                "id": f"FIN-{self.fake.random_int(min=1000, max=9999)}",
                "title": f"{self.fake.sentence(nb_words=5)}",
                "description": f"Detailed finance issue: {self.fake.text(max_nb_chars=300)}",
                "severity": random.choice(["low", "medium", "high", "critical"]),
                "status": random.choice(["open", "in_progress", "resolved", "closed"]),
                "priority": f"p{random.randint(1, 4)}",
                "reporter": random.choice(["Customer Service", "Risk Team", "Compliance Team", "IT Support", "Operations"]),
                "assignee": random.choice(["payment-team", "fraud-team", "compliance-team", "risk-team", "operations-team"]),
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": [random.choice(self.focus_areas), random.choice(self.regulations), random.choice(self.products)],
                "product": random.choice(self.products)
            })
        
        return tickets
    
    def generate_configs(self, output_dir: Path, volume: str):
        """Generate finance configuration files"""
        print(f"  Generating {volume} finance configuration files...")
        
        configs = []
        
        if volume == "small":
            configs = self._generate_small_configs()
        elif volume == "medium":
            configs = self._generate_medium_configs()
        else:  # large
            configs = self._generate_large_configs()
        
        # Write to files
        for i, config in enumerate(configs):
            (output_dir / f"finance_config_{i+1}.yaml").write_text(config)
        
        print(f" Generated {len(configs)} configuration files")
    
    def _generate_small_configs(self) -> List[str]:
        """Generate small set of finance configs"""
        return [
            f"# Payment Processing Configuration\n"
            f"payment_processing:\n"
            f"  enabled: true\n"
            f"  provider: \"Stripe\"\n"
            f"  api_key: \"sk_test_...\"\n"
            f"  webhook_secret: \"whsec_...\"\n"
            f"  currencies:\n"
            f"    - USD\n"
            f"    - EUR\n"
            f"    - GBP\n"
            f"  limits:\n"
            f"    max_amount: 10000\n"
            f"    daily_limit: 50000\n"
            f"    monthly_limit: 1000000",
            
            f"# Risk Management Settings\n"
            f"risk_management:\n"
            f"  enabled: true\n"
            f"  risk_models:\n"
            f"    - credit_risk\n"
            f"    - fraud_detection\n"
            f"    - market_risk\n"
            f"  thresholds:\n"
            f"    high_risk_score: 80\n"
            f"    medium_risk_score: 50\n"
            f"    low_risk_score: 20\n"
            f"  actions:\n"
            f"    auto_block: true\n"
            f"    manual_review: true\n"
            f"    customer_notification: true",
            
            f"# Compliance Configuration\n"
            f"compliance:\n"
            f"  regulations:\n"
            f"    - {self.regulations[0].upper()}\n"
            f"    - {self.regulations[1].upper()}\n"
            f"    - {self.regulations[2].upper()}\n"
            f"  reporting:\n"
            f"    frequency: monthly\n"
            f"    format: pdf\n"
            f"    recipients:\n"
            f"      - compliance@company.com\n"
            f"      - legal@company.com\n"
            f"  audit:\n"
            f"    frequency: quarterly\n"
            f"    scope: full\n"
            f"    retention: 7_years"
        ]
    
    def _generate_medium_configs(self) -> List[str]:
        """Generate medium set of finance configs"""
        configs = self._generate_small_configs()
        
        # Add more configs
        configs.extend([
            f"# Fraud Detection System\n"
            f"fraud_detection:\n"
            f"  enabled: true\n"
            f"  models:\n"
            f"    - ml_model_v1\n"
            f"    - rule_based_v2\n"
            f"    - behavioral_analysis\n"
            f"  features:\n"
            f"    - transaction_amount\n"
            f"    - location\n"
            f"    - device_fingerprint\n"
            f"    - user_behavior\n"
            f"  alerts:\n"
            f"    email: fraud-alerts@company.com\n"
            f"    slack: #fraud-alerts\n"
            f"    webhook: https://alerts.company.com/fraud",
            
            f"# Investment Management\n"
            f"investment_management:\n"
            f"  enabled: true\n"
            f"  portfolio_types:\n"
            f"    - conservative\n"
            f"    - balanced\n"
            f"    - aggressive\n"
            f"  rebalancing:\n"
            f"    frequency: quarterly\n"
            f"    threshold: 5%\n"
            f"    auto_execute: true\n"
            f"  reporting:\n"
            f"    performance: daily\n"
            f"    risk_metrics: weekly\n"
            f"    compliance: monthly"
        ])
        
        return configs
    
    def _generate_large_configs(self) -> List[str]:
        """Generate large set of finance configs"""
        configs = self._generate_medium_configs()
        
        # Add extensive configs
        for product in self.products:
            configs.append(f"# {product.title()} Product Configuration\n"
                         f"{product.lower()}:\n"
                         f"  product_id: {product.upper()}_001\n"
                         f"  manager: {self.fake.name()}\n"
                         f"  features:\n"
                         f"    - core_services\n"
                         f"    - premium_features\n"
                         f"    - analytics\n"
                         f"  pricing:\n"
                         f"    base_fee: {random.randint(10, 100)}\n"
                         f"    transaction_fee: {random.uniform(0.01, 0.05):.3f}\n"
                         f"    monthly_fee: {random.randint(5, 50)}\n"
                         f"  limits:\n"
                         f"    min_balance: {random.randint(100, 1000)}\n"
                         f"    max_transaction: {random.randint(1000, 10000)}\n"
                         f"    daily_limit: {random.randint(5000, 50000)}")
        
        return configs
    
    def generate_chat_history(self, output_dir: Path, volume: str):
        """Generate finance chat history"""
        print(f" Generating {volume} finance chat history...")
        
        conversations = []
        
        if volume == "small":
            conversations = self._generate_small_conversations()
        elif volume == "medium":
            conversations = self._generate_medium_conversations()
        else:  # large
            conversations = self._generate_large_conversations()
        
        # Write to files
        for i, conversation in enumerate(conversations):
            (output_dir / f"finance_chat_{i+1}.json").write_text(json.dumps(conversation, indent=2))
        
        print(f" Generated {len(conversations)} chat conversations")
    
    def _generate_small_conversations(self) -> List[Dict[str, Any]]:
        """Generate small set of finance conversations"""
        return [
            {
                "user_id": "customer_service_rep",
                "session_id": self.fake.uuid4(),
                "messages": [
                    {"role": "user", "message": "Customer reports payment failure, how do I troubleshoot?"},
                    {"role": "assistant", "message": "For payment failures, check:\n1. Transaction status in the system\n2. Error codes and messages\n3. Customer account status\n4. Payment method validity\n\nCommon issues include insufficient funds, expired cards, or system errors."},
                    {"role": "user", "message": "What about fraud detection alerts?"},
                    {"role": "assistant", "message": "For fraud alerts:\n1. Review transaction details\n2. Check customer history\n3. Verify identity if needed\n4. Contact fraud team if suspicious\n\nNever process transactions that trigger fraud alerts without verification."}
                ],
                "timestamp": self.fake.date_time_this_month().isoformat(),
                "product": random.choice(self.products)
            },
            {
                "user_id": "risk_analyst",
                "session_id": self.fake.uuid4(),
                "messages": [
                    {"role": "user", "message": "How do I configure risk thresholds?"},
                    {"role": "assistant", "message": "Risk thresholds can be configured in the risk management system:\n1. Access risk configuration\n2. Set score thresholds\n3. Define action triggers\n4. Test with sample data\n\nRecommended thresholds: High (80+), Medium (50-79), Low (0-49)"},
                    {"role": "user", "message": "What about compliance reporting?"},
                    {"role": "assistant", "message": "Compliance reporting includes:\n1. Monthly transaction reports\n2. Risk assessment summaries\n3. Audit trail documentation\n4. Regulatory filings\n\nEnsure all reports are generated on time and reviewed for accuracy."}
                ],
                "timestamp": self.fake.date_time_this_month().isoformat(),
                "product": random.choice(self.products)
            }
        ]
    
    def _generate_medium_conversations(self) -> List[Dict[str, Any]]:
        """Generate medium set of finance conversations"""
        conversations = self._generate_small_conversations()
        
        # Add more conversations
        for i in range(3):
            conversations.append({
                "user_id": f"finance_user_{i+1}",
                "session_id": self.fake.uuid4(),
                "messages": [
                    {"role": "user", "message": f"How do I set up {random.choice(self.focus_areas)}?"},
                    {"role": "assistant", "message": f"Setting up {random.choice(self.focus_areas)} involves several steps. Let me guide you through the process."},
                    {"role": "user", "message": "What are the compliance requirements?"},
                    {"role": "assistant", "message": f"The compliance requirements include {random.choice(self.regulations).upper()} standards and regular audits."},
                    {"role": "user", "message": "Thanks for the help!"},
                    {"role": "assistant", "message": "You're welcome! Feel free to ask if you need any clarification."}
                ],
                "timestamp": self.fake.date_time_this_month().isoformat(),
                "product": random.choice(self.products)
            })
        
        return conversations
    
    def _generate_large_conversations(self) -> List[Dict[str, Any]]:
        """Generate large set of finance conversations"""
        conversations = self._generate_medium_conversations()
        
        # Add many more conversations
        for i in range(10):
            conversations.append({
                "user_id": f"finance_user_{i+10}",
                "session_id": self.fake.uuid4(),
                "messages": [
                    {"role": "user", "message": f"I need help with {random.choice(self.focus_areas)}"},
                    {"role": "assistant", "message": f"I'd be happy to help you with {random.choice(self.focus_areas)}. What specific issue are you facing?"},
                    {"role": "user", "message": f"The system is showing {random.choice(self.regulations)} compliance error"},
                    {"role": "assistant", "message": f"For {random.choice(self.regulations).upper()} compliance issues, here are some steps:\n1. Review current policies\n2. Check system configurations\n3. Verify staff training\n4. Contact compliance team if needed"},
                    {"role": "user", "message": "Can you provide more specific guidance?"},
                    {"role": "assistant", "message": f"Certainly! For {random.choice(self.focus_areas)} issues, you should:\n- Check the documentation\n- Review compliance requirements\n- Test with minimal setup\n- Contact support if needed"}
                ],
                "timestamp": self.fake.date_time_this_month().isoformat(),
                "product": random.choice(self.products)
            })
        
        return conversations
