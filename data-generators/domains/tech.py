"""
Tech Domain Data Generator

Generates synthetic data for technology-focused RAG chatbot demo.
Includes API documentation, system configurations, support tickets, and chat history.
"""

from faker import Faker
from pathlib import Path
from typing import List, Dict, Any
import random
import json

class TechDataGenerator:
    """Generator for tech domain data"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.fake = Faker()
        self.domain_config = config["data_generation"].get("tech", {})
        self.focus_areas = self.domain_config.get("focus_areas", ["api", "database", "authentication"])
        self.tech_stack = self.domain_config.get("tech_stack", ["python", "fastapi", "postgresql"])
        self.common_issues = self.domain_config.get("common_issues", ["timeout", "authentication", "database_connection"])
        self.environments = ["staging", "production", "sandbox"]
        self.support_teams = ["tech-support", "backend-team", "frontend-team", "devops-team"]
        
    def generate_docs(self, output_dir: Path, volume: str):
        """Generate technical documentation"""
        print(f" Generating {volume} tech documentation...")
        
        docs = []
        
        if volume == "small":
            docs = self._generate_small_docs()
        elif volume == "medium":
            docs = self._generate_medium_docs()
        else:  # large
            docs = self._generate_large_docs()
        
        # Write to files
        for i, doc in enumerate(docs):
            (output_dir / f"tech_doc_{i+1}.md").write_text(doc)
        
        print(f" Generated {len(docs)} documentation files")
    
    def _generate_small_docs(self) -> List[str]:
        """Generate small set of technical docs"""
        return [
            f"# {self.focus_areas[0].title()} Configuration\n\n"
            f"To configure {self.focus_areas[0]}, set the following in your config:\n\n"
            f"```yaml\n{self.tech_stack[0]}_config:\n  enabled: true\n  timeout: 30\n  retries: 3\n```\n\n"
            f"## Prerequisites\n- {self.tech_stack[1]} installed\n- {self.tech_stack[2]} configured\n\n"
            f"## Usage\nUse the `{self.focus_areas[0]}` endpoint to interact with the system.",
            
            f"# {self.focus_areas[1].title()} Setup\n\n"
            f"Setting up {self.focus_areas[1]} requires:\n\n"
            f"1. Install {self.tech_stack[1]}\n"
            f"2. Configure connection string\n"
            f"3. Test connectivity\n"
            f"4. Set up monitoring\n\n"
            f"## Configuration\n```json\n{{\n  \"host\": \"localhost\",\n  \"port\": 5432,\n  \"database\": \"app_db\"\n}}\n```",
            
            f"# Troubleshooting {self.focus_areas[0]}\n\n"
            f"Common issues and solutions:\n\n"
            f"## Issue 1: Connection timeout\n**Symptoms**: Requests fail after 30 seconds\n"
            f"**Solution**: Increase timeout value in config\n\n"
            f"## Issue 2: Authentication failure\n**Symptoms**: 401 Unauthorized errors\n"
            f"**Solution**: Check credentials and permissions\n\n"
            f"## Issue 3: {self.common_issues[0]}\n**Symptoms**: System unresponsive\n"
            f"**Solution**: Check system resources and logs"
        ]
    
    def _generate_medium_docs(self) -> List[str]:
        """Generate medium set of technical docs"""
        docs = self._generate_small_docs()
        
        # Add more comprehensive docs
        docs.extend([
            f"# {self.focus_areas[2].title()} Guide\n\n"
            f"Complete guide to {self.focus_areas[2]} implementation:\n\n"
            f"## Prerequisites\n- {self.tech_stack[0]} installed\n- {self.tech_stack[1]} configured\n- {self.tech_stack[2]} running\n\n"
            f"## Implementation\n```python\n# Example code\nconfig = {{\n  'auth_mode': 'hybrid',\n  'timeout': 30,\n  'retries': 3\n}}\n\n# Initialize client\nclient = {self.tech_stack[1].title()}Client(config)\n```\n\n"
            f"## API Endpoints\n- `GET /api/v1/{self.focus_areas[0]}` - List all items\n"
            f"- `POST /api/v1/{self.focus_areas[0]}` - Create new item\n"
            f"- `PUT /api/v1/{self.focus_areas[0]}/{{id}}` - Update item\n"
            f"- `DELETE /api/v1/{self.focus_areas[0]}/{{id}}` - Delete item",
            
            f"# {self.focus_areas[3].title()} Best Practices\n\n"
            f"Best practices for {self.focus_areas[3]}:\n\n"
            f"## Security\n- Use HTTPS for all communications\n- Implement proper authentication\n- Validate all inputs\n- Use environment variables for secrets\n\n"
            f"## Performance\n- Implement caching where appropriate\n- Use connection pooling\n- Monitor resource usage\n- Optimize database queries\n\n"
            f"## Monitoring\n- Set up health checks\n- Monitor error rates\n- Track performance metrics\n- Set up alerts",
            
            f"# API Reference\n\n"
            f"Complete API reference for {self.focus_areas[0]}:\n\n"
            f"## Authentication\nAll API requests require authentication via JWT token:\n"
            f"```bash\ncurl -H \"Authorization: Bearer <token>\" \\\n  https://api.example.com/v1/{self.focus_areas[0]}\n```\n\n"
            f"## Response Format\nAll responses follow this format:\n"
            f"```json\n{{\n  \"status\": \"success\",\n  \"data\": {{}},\n  \"message\": \"Operation completed\"\n}}\n```\n\n"
            f"## Error Codes\n- `400`: Bad Request\n- `401`: Unauthorized\n- `403`: Forbidden\n- `404`: Not Found\n- `500`: Internal Server Error"
        ])
        
        return docs
    
    def _generate_large_docs(self) -> List[str]:
        """Generate large set of technical docs"""
        docs = self._generate_medium_docs()
        
        # Add extensive documentation
        for area in self.focus_areas:
            docs.append(f"# Advanced {area.title()}\n\n"
                       f"Advanced configuration and optimization for {area}:\n\n"
                       f"## Performance Tuning\n- Optimize queries\n- Cache frequently accessed data\n- Use indexes effectively\n- Monitor query performance\n\n"
                       f"## Security Considerations\n- Implement proper authentication\n- Use encryption for sensitive data\n- Regular security audits\n- Keep dependencies updated\n\n"
                       f"## Integration Patterns\n- Microservices architecture\n- Event-driven design\n- Circuit breaker pattern\n- Retry mechanisms")
        
        # Add more specific tech stack docs
        for tech in self.tech_stack:
            docs.append(f"# {tech.title()} Integration\n\n"
                       f"Integration guide for {tech}:\n\n"
                       f"## Installation\n```bash\npip install {tech}\n```\n\n"
                       f"## Configuration\n```python\nimport {tech}\n\n# Configure client\nclient = {tech}.Client(\n    host='localhost',\n    port=8080\n)\n```\n\n"
                       f"## Usage Examples\n- Basic operations\n- Error handling\n- Best practices")
        
        return docs
    
    def generate_tickets(self, output_dir: Path, volume: str):
        """Generate support tickets"""
        print(f" Generating {volume} tech support tickets...")
        
        tickets = []
        
        if volume == "small":
            tickets = self._generate_small_tickets()
        elif volume == "medium":
            tickets = self._generate_medium_tickets()
        else:  # large
            tickets = self._generate_large_tickets()
        
        # Write to files
        for i, ticket in enumerate(tickets):
            (output_dir / f"tech_ticket_{i+1}.json").write_text(json.dumps(ticket, indent=2))
        
        print(f" Generated {len(tickets)} support tickets")
    
    def _generate_small_tickets(self) -> List[Dict[str, Any]]:
        """Generate small set of support tickets"""
        return [
            {
                "id": f"TECH-{self.fake.random_int(min=1000, max=9999)}",
                "title": f"User unable to authenticate with {self.focus_areas[0]}",
                "description": f"User reports 401 error when trying to access {self.focus_areas[0]} endpoint. JWT token appears to be valid but authentication fails.",
                "severity": "high",
                "status": "open",
                "priority": "p2",
                "reporter": self.fake.name(),
                "assignee": "tech-support",
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": [self.focus_areas[0], "authentication", "jwt"]
            },
            {
                "id": f"TECH-{self.fake.random_int(min=1000, max=9999)}",
                "title": f"{self.tech_stack[0]} connection timeout",
                "description": f"Application fails to connect to {self.tech_stack[0]} after 30 seconds. Connection string appears correct.",
                "severity": "medium",
                "status": "in_progress",
                "priority": "p3",
                "reporter": self.fake.name(),
                "assignee": "backend-team",
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": [self.tech_stack[0], "connection", "timeout"]
            },
            {
                "id": f"TECH-{self.fake.random_int(min=1000, max=9999)}",
                "title": f"Database query performance issue",
                "description": f"Queries against {self.focus_areas[1]} are taking longer than expected. Some queries exceed 5 seconds.",
                "severity": "medium",
                "status": "open",
                "priority": "p3",
                "reporter": self.fake.name(),
                "assignee": "dba-team",
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": [self.focus_areas[1], "performance", "database"]
            }
        ]
    
    def _generate_medium_tickets(self) -> List[Dict[str, Any]]:
        """Generate medium set of support tickets"""
        tickets = self._generate_small_tickets()
        for _ in range(5):
            tickets.append(self._build_template_ticket())
        return tickets
    
    def _build_template_ticket(self) -> Dict[str, Any]:
        """Create a realistic support ticket using structured templates."""
        component = random.choice(self.focus_areas)
        environment = random.choice(self.environments)
        reporter = self.fake.name()
        scenario = random.choice(["timeout", "auth", "deployment", "config_drift", "data_integrity"])
        severity = random.choice(["low", "medium", "high", "critical"])
        priority = f"p{random.randint(1, 4)}"
        status = random.choice(["open", "in_progress", "resolved"])
        ticket = {
            "id": f"TECH-{self.fake.random_int(min=1000, max=9999)}",
            "severity": severity,
            "status": status,
            "priority": priority,
            "reporter": reporter,
            "assignee": random.choice(self.support_teams),
            "created_at": self.fake.date_time_this_month().isoformat(),
        }

        if scenario == "timeout":
            sla = random.choice(["2s", "5s", "10s"])
            ticket.update(
                {
                    "title": f"{component.title()} requests timing out in {environment}",
                    "description": (
                        f"{reporter} reports repeated HTTP 504 responses when calling the {component} endpoint in {environment}. "
                        f"P95 latency exceeds the {sla} SLA even after scaling the service and clearing caches. "
                        f"They need guidance on profiling the slow path and whether to raise the client timeout."
                    ),
                    "tags": [component, "timeout", environment],
                }
            )
        elif scenario == "auth":
            failure_rate = random.choice(["20%", "35%", "50%"])
            ticket.update(
                {
                    "title": f"{component.title()} authentication failures for existing users",
                    "description": (
                        f"{reporter} cannot reproduce customer logins because {failure_rate} of requests return 401 in {environment}. "
                        f"Tokens appear valid and reissuing them does not help. They need recommendations on debugging the "
                        f"{component} policy engine and verifying recent secret rotations."
                    ),
                    "tags": [component, "authentication", environment],
                }
            )
        elif scenario == "deployment":
            step = random.choice(["migrate database", "run smoke tests", "register service"])
            ticket.update(
                {
                    "title": f"Deployment to {environment} fails during {step}",
                    "description": (
                        f"The {component} deployment pipeline aborts while trying to {step} in {environment}. "
                        f"Build logs show the new container never reaches a healthy state. Reporter already rolled back "
                        f"and wants a checklist for fixing the pipeline safely."
                    ),
                    "tags": [component, "deployment", environment],
                }
            )
        elif scenario == "config_drift":
            flag = random.choice(["FEATURE_BETA", "AUTH_BYPASS", "RATE_LIMITER"])
            ticket.update(
                {
                    "title": f"Config drift detected for {component} between environments",
                    "description": (
                        f"{component.title()} behaves differently between {environment} and production. "
                        f"Flag `{flag}` is enabled in one environment and disabled in the other, causing inconsistent results. "
                        f"The team needs guidance on aligning config maps and preventing future drift."
                    ),
                    "tags": [component, "config", environment],
                }
            )
        else:
            rows = random.randint(50, 500)
            ticket.update(
                {
                    "title": f"Data integrity issues detected in {component}",
                    "description": (
                        f"{reporter} found {rows} records with mismatched checksums after the nightly ETL job in {environment}. "
                        f"Preliminary investigation shows the pipeline skipped a validation step. They need an action plan for "
                        f"quarantining the bad data and reprocessing the feed."
                    ),
                    "tags": [component, "data-quality", environment],
                }
            )

        return ticket

    def _generate_large_tickets(self) -> List[Dict[str, Any]]:
        """Generate large set of support tickets"""
        tickets = self._generate_medium_tickets()
        for _ in range(20):
            tickets.append(self._build_template_ticket())
        return tickets

    def generate_configs(self, output_dir: Path, volume: str):
        """Generate configuration files"""
        print(f"  Generating {volume} tech configuration files...")
        
        configs = []
        
        if volume == "small":
            configs = self._generate_small_configs()
        elif volume == "medium":
            configs = self._generate_medium_configs()
        else:  # large
            configs = self._generate_large_configs()
        
        # Write to files
        for i, config in enumerate(configs):
            (output_dir / f"tech_config_{i+1}.yaml").write_text(config)
        
        print(f" Generated {len(configs)} configuration files")
    
    def _generate_small_configs(self) -> List[str]:
        """Generate small set of configuration files"""
        return [
            f"# {self.focus_areas[0].title()} Configuration\n"
            f"auth_mode: hybrid\n"
            f"user_id: dev123\n"
            f"fallback: true\n"
            f"timeout: 30\n"
            f"retries: 3\n"
            f"debug: false\n"
            f"log_level: info",
            
            f"# {self.tech_stack[0].title()} Settings\n"
            f"database:\n"
            f"  host: localhost\n"
            f"  port: 5432\n"
            f"  name: app_db\n"
            f"  user: app_user\n"
            f"  password: secret\n"
            f"  pool_size: 10\n"
            f"  max_overflow: 20",
            
            f"# API Configuration\n"
            f"api:\n"
            f"  version: v1\n"
            f"  base_url: https://api.example.com\n"
            f"  rate_limit: 1000\n"
            f"  timeout: 30\n"
            f"  retries: 3\n"
            f"  cache_ttl: 300"
        ]
    
    def _generate_medium_configs(self) -> List[str]:
        """Generate medium set of configuration files"""
        configs = self._generate_small_configs()
        
        # Add more configs
        configs.extend([
            f"# {self.focus_areas[1].title()} Setup\n"
            f"monitoring:\n"
            f"  enabled: true\n"
            f"  metrics_endpoint: /metrics\n"
            f"  health_check: /health\n"
            f"  alerting:\n"
            f"    email: admin@example.com\n"
            f"    webhook: https://hooks.slack.com/...\n"
            f"  thresholds:\n"
            f"    cpu: 80\n"
            f"    memory: 85\n"
            f"    disk: 90",
            
            f"# Security Configuration\n"
            f"security:\n"
            f"  jwt:\n"
            f"    secret: {self.fake.password()}\n"
            f"    algorithm: HS256\n"
            f"    expires_in: 3600\n"
            f"  cors:\n"
            f"    origins: ['https://app.example.com']\n"
            f"    methods: ['GET', 'POST', 'PUT', 'DELETE']\n"
            f"    headers: ['Content-Type', 'Authorization']\n"
            f"  rate_limiting:\n"
            f"    enabled: true\n"
            f"    requests_per_minute: 100"
        ])
        
        return configs
    
    def _generate_large_configs(self) -> List[str]:
        """Generate large set of configuration files"""
        configs = self._generate_medium_configs()
        
        # Add extensive configs
        for tech in self.tech_stack:
            configs.append(f"# {tech.title()} Configuration\n"
                         f"{tech}:\n"
                         f"  enabled: true\n"
                         f"  host: localhost\n"
                         f"  port: {random.randint(8000, 9000)}\n"
                         f"  timeout: 30\n"
                         f"  retries: 3\n"
                         f"  pool_size: 10\n"
                         f"  max_connections: 100\n"
                         f"  ssl:\n"
                         f"    enabled: true\n"
                         f"    cert_file: /path/to/cert.pem\n"
                         f"    key_file: /path/to/key.pem")
        
        return configs
    
    def generate_chat_history(self, output_dir: Path, volume: str):
        """Generate chat history"""
        print(f" Generating {volume} tech chat history...")
        
        conversations = []
        
        if volume == "small":
            conversations = self._generate_small_conversations()
        elif volume == "medium":
            conversations = self._generate_medium_conversations()
        else:  # large
            conversations = self._generate_large_conversations()
        
        # Write to files
        for i, conversation in enumerate(conversations):
            (output_dir / f"tech_chat_{i+1}.json").write_text(json.dumps(conversation, indent=2))
        
        print(f" Generated {len(conversations)} chat conversations")
    
    def _generate_small_conversations(self) -> List[Dict[str, Any]]:
        """Generate small set of chat conversations"""
        return [
            {
                "user_id": "dev_user_1",
                "session_id": self.fake.uuid4(),
                "messages": [
                    {"role": "user", "message": f"How do I configure {self.focus_areas[0]}?"},
                    {"role": "assistant", "message": f"To configure {self.focus_areas[0]}, you need to set the appropriate parameters in your config file. Here's an example:\n\n```yaml\n{self.focus_areas[0]}:\n  enabled: true\n  timeout: 30\n```"},
                    {"role": "user", "message": "What happens if the timeout is too low?"},
                    {"role": "assistant", "message": "If the timeout is too low, you may experience connection failures. I recommend setting it to at least 30 seconds for most use cases."}
                ],
                "timestamp": self.fake.date_time_this_month().isoformat()
            },
            {
                "user_id": "admin_user_1",
                "session_id": self.fake.uuid4(),
                "messages": [
                    {"role": "user", "message": f"I'm having issues with {self.tech_stack[0]} performance"},
                    {"role": "assistant", "message": f"Let me help you troubleshoot {self.tech_stack[0]} performance issues. Can you share more details about what you're experiencing?"},
                    {"role": "user", "message": "Queries are taking longer than expected"},
                    {"role": "assistant", "message": "For query performance issues, I recommend:\n1. Check if indexes are properly configured\n2. Review query execution plans\n3. Monitor resource usage\n4. Consider query optimization"}
                ],
                "timestamp": self.fake.date_time_this_month().isoformat()
            }
        ]
    
    def _generate_medium_conversations(self) -> List[Dict[str, Any]]:
        """Generate medium set of chat conversations"""
        conversations = self._generate_small_conversations()
        
        # Prepare shuffled topics to avoid duplicate conversations
        focus_cycle = list(self.focus_areas)
        tech_cycle = list(self.tech_stack)
        random.shuffle(focus_cycle)
        random.shuffle(tech_cycle)
        
        # Add more conversations
        for i in range(3):
            focus_topic = focus_cycle[i % len(focus_cycle)]
            tech_topic = tech_cycle[i % len(tech_cycle)]
            conversations.append({
                "user_id": f"user_{i+1}",
                "session_id": self.fake.uuid4(),
                "messages": [
                    {"role": "user", "message": f"How do I set up {focus_topic}?"},
                    {"role": "assistant", "message": f"Setting up {focus_topic} involves several steps. Let me guide you through the process."},
                    {"role": "user", "message": "What are the prerequisites?"},
                    {"role": "assistant", "message": f"The prerequisites include installing {tech_topic} and configuring the necessary settings."},
                    {"role": "user", "message": "Thanks for the help!"},
                    {"role": "assistant", "message": "You're welcome! Feel free to ask if you need any clarification."}
                ],
                "timestamp": self.fake.date_time_this_month().isoformat()
            })
        
        return conversations
    
    def _generate_large_conversations(self) -> List[Dict[str, Any]]:
        """Generate large set of chat conversations"""
        conversations = self._generate_medium_conversations()
        
        # Add many more conversations
        for i in range(10):
            conversations.append({
                "user_id": f"user_{i+10}",
                "session_id": self.fake.uuid4(),
                "messages": [
                    {"role": "user", "message": f"I need help with {random.choice(self.focus_areas)}"},
                    {"role": "assistant", "message": f"I'd be happy to help you with {random.choice(self.focus_areas)}. What specific issue are you facing?"},
                    {"role": "user", "message": f"The system is showing {random.choice(self.common_issues)} error"},
                    {"role": "assistant", "message": f"For {random.choice(self.common_issues)} errors, here are some troubleshooting steps:\n1. Check system logs\n2. Verify configuration\n3. Test connectivity\n4. Review error messages"},
                    {"role": "user", "message": "Can you provide more specific guidance?"},
                    {"role": "assistant", "message": f"Certainly! For {random.choice(self.focus_areas)} issues, you should:\n- Check the documentation\n- Review configuration files\n- Test with minimal setup\n- Contact support if needed"}
                ],
                "timestamp": self.fake.date_time_this_month().isoformat()
            })
        
        return conversations
