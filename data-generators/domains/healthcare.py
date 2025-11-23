"""
Healthcare Domain Data Generator

Generates synthetic data for healthcare-focused RAG chatbot demo.
Includes medical protocols, HIPAA compliance, patient records, and healthcare chat history.
"""

from faker import Faker
from pathlib import Path
from typing import List, Dict, Any
import random
import json

class HealthcareDataGenerator:
    """Generator for healthcare domain data"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.fake = Faker()
        self.domain_config = config["data_generation"].get("healthcare", {})
        self.focus_areas = self.domain_config.get("focus_areas", ["patient_records", "hipaa", "medical_protocols"])
        self.specialties = self.domain_config.get("specialties", ["cardiology", "oncology", "emergency"])
        self.compliance_standards = self.domain_config.get("compliance_standards", ["hipaa", "fda", "joint_commission"])
        
    def generate_docs(self, output_dir: Path, volume: str):
        """Generate healthcare documentation"""
        print(f" Generating {volume} healthcare documentation...")
        
        docs = []
        
        if volume == "small":
            docs = self._generate_small_docs()
        elif volume == "medium":
            docs = self._generate_medium_docs()
        else:  # large
            docs = self._generate_large_docs()
        
        # Write to files
        for i, doc in enumerate(docs):
            (output_dir / f"healthcare_doc_{i+1}.md").write_text(doc)
        
        print(f" Generated {len(docs)} documentation files")
    
    def _generate_small_docs(self) -> List[str]:
        """Generate small set of healthcare docs"""
        return [
            f"# {self.focus_areas[0].title()} Management\n\n"
            f"Patient records must be maintained according to {self.compliance_standards[0].upper()} guidelines.\n\n"
            f"## Key Requirements\n- Secure storage and access\n- Audit trail maintenance\n- Patient consent management\n- Data encryption at rest and in transit\n\n"
            f"## Access Controls\n- Role-based access permissions\n- Multi-factor authentication\n- Regular access reviews\n- Incident logging and monitoring",
            
            f"# {self.specialties[0].title()} Protocols\n\n"
            f"Standard protocols for {self.specialties[0]} care:\n\n"
            f"## Patient Assessment\n1. Initial evaluation\n2. Diagnostic testing\n3. Treatment planning\n4. Follow-up care\n\n"
            f"## Documentation Requirements\n- Clinical notes\n- Test results\n- Treatment plans\n- Patient communications\n\n"
            f"## Quality Measures\n- Patient outcomes\n- Safety metrics\n- Compliance tracking\n- Continuous improvement",
            
            f"# {self.compliance_standards[0].upper()} Compliance Guide\n\n"
            f"Comprehensive guide to {self.compliance_standards[0].upper()} compliance:\n\n"
            f"## Administrative Safeguards\n- Security officer designation\n- Workforce training\n- Access management\n- Incident response\n\n"
            f"## Physical Safeguards\n- Facility access controls\n- Workstation security\n- Device and media controls\n- Disposal procedures\n\n"
            f"## Technical Safeguards\n- Access control systems\n- Audit controls\n- Integrity controls\n- Transmission security"
        ]
    
    def _generate_medium_docs(self) -> List[str]:
        """Generate medium set of healthcare docs"""
        docs = self._generate_small_docs()
        
        # Add more comprehensive docs
        docs.extend([
            f"# Telemedicine Implementation\n\n"
            f"Guidelines for implementing telemedicine services:\n\n"
            f"## Technology Requirements\n- Secure video conferencing platform\n- Electronic health record integration\n- Patient portal access\n- Mobile device compatibility\n\n"
            f"## Clinical Standards\n- Provider licensing and credentials\n- Patient identification and consent\n- Clinical documentation\n- Follow-up care protocols\n\n"
            f"## Security Considerations\n- End-to-end encryption\n- Secure data transmission\n- Patient privacy protection\n- Compliance with regulations",
            
            f"# Medical Device Integration\n\n"
            f"Integration of medical devices with electronic health records:\n\n"
            f"## Device Types\n- Monitoring devices\n- Diagnostic equipment\n- Treatment devices\n- Mobile health apps\n\n"
            f"## Integration Standards\n- HL7 FHIR compliance\n- DICOM for imaging\n- IEEE 11073 for device communication\n- Interoperability requirements\n\n"
            f"## Data Management\n- Real-time data capture\n- Data validation and quality\n- Storage and retention\n- Analytics and reporting",
            
            f"# Emergency Response Protocols\n\n"
            f"Emergency response procedures for healthcare facilities:\n\n"
            f"## Incident Types\n- Medical emergencies\n- System failures\n- Security breaches\n- Natural disasters\n\n"
            f"## Response Teams\n- Emergency response team\n- IT support team\n- Clinical staff\n- Administration\n\n"
            f"## Communication\n- Internal notifications\n- External communications\n- Patient and family updates\n- Regulatory reporting"
        ])
        
        return docs
    
    def _generate_large_docs(self) -> List[str]:
        """Generate large set of healthcare docs"""
        docs = self._generate_medium_docs()
        
        # Add extensive documentation
        for specialty in self.specialties:
            docs.append(f"# {specialty.title()} Clinical Guidelines\n\n"
                       f"Clinical guidelines for {specialty} care:\n\n"
                       f"## Assessment Protocols\n- Initial patient evaluation\n- Diagnostic criteria\n- Risk stratification\n- Treatment planning\n\n"
                       f"## Treatment Options\n- Medical management\n- Surgical interventions\n- Rehabilitation services\n- Palliative care\n\n"
                       f"## Quality Indicators\n- Patient outcomes\n- Safety measures\n- Efficiency metrics\n- Patient satisfaction")
        
        # Add compliance documentation
        for standard in self.compliance_standards:
            docs.append(f"# {standard.upper()} Compliance Framework\n\n"
                       f"Comprehensive compliance framework for {standard.upper()}:\n\n"
                       f"## Requirements\n- Regulatory requirements\n- Implementation guidelines\n- Monitoring procedures\n- Reporting obligations\n\n"
                       f"## Risk Management\n- Risk assessment\n- Mitigation strategies\n- Monitoring and review\n- Continuous improvement\n\n"
                       f"## Training and Education\n- Staff training programs\n- Competency assessment\n- Ongoing education\n- Certification requirements")
        
        return docs
    
    def generate_tickets(self, output_dir: Path, volume: str):
        """Generate healthcare support tickets"""
        print(f" Generating {volume} healthcare support tickets...")
        
        tickets = []
        
        if volume == "small":
            tickets = self._generate_small_tickets()
        elif volume == "medium":
            tickets = self._generate_medium_tickets()
        else:  # large
            tickets = self._generate_large_tickets()
        
        # Write to files
        for i, ticket in enumerate(tickets):
            (output_dir / f"healthcare_ticket_{i+1}.json").write_text(json.dumps(ticket, indent=2))
        
        print(f" Generated {len(tickets)} support tickets")
    
    def _generate_small_tickets(self) -> List[Dict[str, Any]]:
        """Generate small set of healthcare tickets"""
        return [
            {
                "id": f"HC-{self.fake.random_int(min=1000, max=9999)}",
                "title": "Patient record access issue",
                "description": "Healthcare provider unable to access patient records through EHR system. Error message indicates permission denied.",
                "severity": "high",
                "status": "open",
                "priority": "p1",
                "reporter": "Dr. " + self.fake.last_name(),
                "assignee": "healthcare-it",
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": ["patient_records", "access_control", "ehr"],
                "department": random.choice(self.specialties)
            },
            {
                "id": f"HC-{self.fake.random_int(min=1000, max=9999)}",
                "title": "HIPAA compliance audit findings",
                "description": "Recent HIPAA audit identified several compliance gaps in patient data handling procedures.",
                "severity": "critical",
                "status": "in_progress",
                "priority": "p1",
                "reporter": "Compliance Officer",
                "assignee": "compliance-team",
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": ["hipaa", "compliance", "audit"],
                "department": "compliance"
            },
            {
                "id": f"HC-{self.fake.random_int(min=1000, max=9999)}",
                "title": "Medical device connectivity problem",
                "description": "Cardiology monitoring device not transmitting data to central monitoring system.",
                "severity": "medium",
                "status": "open",
                "priority": "p2",
                "reporter": "Nurse " + self.fake.last_name(),
                "assignee": "biomedical-engineering",
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": ["medical_device", "connectivity", "monitoring"],
                "department": "cardiology"
            }
        ]
    
    def _generate_medium_tickets(self) -> List[Dict[str, Any]]:
        """Generate medium set of healthcare tickets"""
        tickets = self._generate_small_tickets()
        
        # Add more tickets
        for i in range(5):
            tickets.append({
                "id": f"HC-{self.fake.random_int(min=1000, max=9999)}",
                "title": f"{self.fake.sentence(nb_words=4)}",
                "description": f"Healthcare issue reported: {self.fake.text(max_nb_chars=200)}",
                "severity": random.choice(["low", "medium", "high", "critical"]),
                "status": random.choice(["open", "in_progress", "resolved"]),
                "priority": f"p{random.randint(1, 4)}",
                "reporter": random.choice(["Dr. " + self.fake.last_name(), "Nurse " + self.fake.last_name(), "Admin " + self.fake.last_name()]),
                "assignee": random.choice(["healthcare-it", "compliance-team", "biomedical-engineering", "clinical-staff"]),
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": [random.choice(self.focus_areas), random.choice(self.specialties)],
                "department": random.choice(self.specialties)
            })
        
        return tickets
    
    def _generate_large_tickets(self) -> List[Dict[str, Any]]:
        """Generate large set of healthcare tickets"""
        tickets = self._generate_medium_tickets()
        
        # Add many more tickets
        for i in range(20):
            tickets.append({
                "id": f"HC-{self.fake.random_int(min=1000, max=9999)}",
                "title": f"{self.fake.sentence(nb_words=5)}",
                "description": f"Detailed healthcare issue: {self.fake.text(max_nb_chars=300)}",
                "severity": random.choice(["low", "medium", "high", "critical"]),
                "status": random.choice(["open", "in_progress", "resolved", "closed"]),
                "priority": f"p{random.randint(1, 4)}",
                "reporter": random.choice(["Dr. " + self.fake.last_name(), "Nurse " + self.fake.last_name(), "Admin " + self.fake.last_name()]),
                "assignee": random.choice(["healthcare-it", "compliance-team", "biomedical-engineering", "clinical-staff", "administration"]),
                "created_at": self.fake.date_time_this_month().isoformat(),
                "tags": [random.choice(self.focus_areas), random.choice(self.specialties), random.choice(self.compliance_standards)],
                "department": random.choice(self.specialties)
            })
        
        return tickets
    
    def generate_configs(self, output_dir: Path, volume: str):
        """Generate healthcare configuration files"""
        print(f"  Generating {volume} healthcare configuration files...")
        
        configs = []
        
        if volume == "small":
            configs = self._generate_small_configs()
        elif volume == "medium":
            configs = self._generate_medium_configs()
        else:  # large
            configs = self._generate_large_configs()
        
        # Write to files
        for i, config in enumerate(configs):
            (output_dir / f"healthcare_config_{i+1}.yaml").write_text(config)
        
        print(f" Generated {len(configs)} configuration files")
    
    def _generate_small_configs(self) -> List[str]:
        """Generate small set of healthcare configs"""
        return [
            f"# EHR System Configuration\n"
            f"ehr:\n"
            f"  system_name: \"HealthCare EHR\"\n"
            f"  version: \"2.1.0\"\n"
            f"  database:\n"
            f"    host: localhost\n"
            f"    port: 5432\n"
            f"    name: healthcare_db\n"
            f"    ssl: true\n"
            f"  security:\n"
            f"    encryption: true\n"
            f"    audit_logging: true\n"
            f"    session_timeout: 1800",
            
            f"# Patient Portal Settings\n"
            f"patient_portal:\n"
            f"  enabled: true\n"
            f"  url: https://portal.healthcare.com\n"
            f"  features:\n"
            f"    - appointment_scheduling\n"
            f"    - prescription_refills\n"
            f"    - lab_results\n"
            f"    - messaging\n"
            f"  security:\n"
            f"    mfa_required: true\n"
            f"    password_policy: strict\n"
            f"    session_timeout: 900",
            
            f"# HIPAA Compliance Settings\n"
            f"hipaa:\n"
            f"  compliance_mode: strict\n"
            f"  data_retention_years: 7\n"
            f"  audit_retention_years: 6\n"
            f"  encryption:\n"
            f"    at_rest: true\n"
            f"    in_transit: true\n"
            f"    algorithm: AES-256\n"
            f"  access_controls:\n"
            f"    role_based: true\n"
            f"    mfa_required: true\n"
            f"    session_monitoring: true"
        ]
    
    def _generate_medium_configs(self) -> List[str]:
        """Generate medium set of healthcare configs"""
        configs = self._generate_small_configs()
        
        # Add more configs
        configs.extend([
            f"# Medical Device Integration\n"
            f"medical_devices:\n"
            f"  enabled: true\n"
            f"  protocols:\n"
            f"    - HL7_FHIR\n"
            f"    - DICOM\n"
            f"    - IEEE_11073\n"
            f"  devices:\n"
            f"    - patient_monitors\n"
            f"    - infusion_pumps\n"
            f"    - ventilators\n"
            f"    - defibrillators\n"
            f"  data_collection:\n"
            f"    real_time: true\n"
            f"    batch_processing: false\n"
            f"    data_validation: true",
            
            f"# Telemedicine Configuration\n"
            f"telemedicine:\n"
            f"  enabled: true\n"
            f"  platform: \"SecureVideo\"\n"
            f"  features:\n"
            f"    - video_consultations\n"
            f"    - screen_sharing\n"
            f"    - file_sharing\n"
            f"    - recording\n"
            f"  security:\n"
            f"    encryption: end_to_end\n"
            f"    authentication: mfa\n"
            f"    session_recording: true\n"
            f"    data_retention: 30_days"
        ])
        
        return configs
    
    def _generate_large_configs(self) -> List[str]:
        """Generate large set of healthcare configs"""
        configs = self._generate_medium_configs()
        
        # Add extensive configs
        for specialty in self.specialties:
            configs.append(f"# {specialty.title()} Department Configuration\n"
                         f"{specialty.lower()}:\n"
                         f"  department_id: {specialty.upper()}_001\n"
                         f"  head_physician: Dr. {self.fake.last_name()}\n"
                         f"  staff_count: {random.randint(10, 50)}\n"
                         f"  equipment:\n"
                         f"    - monitoring_devices\n"
                         f"    - diagnostic_equipment\n"
                         f"    - treatment_devices\n"
                         f"  protocols:\n"
                         f"    - patient_assessment\n"
                         f"    - treatment_planning\n"
                         f"    - follow_up_care\n"
                         f"  quality_metrics:\n"
                         f"    - patient_outcomes\n"
                         f"    - safety_incidents\n"
                         f"    - efficiency_measures")
        
        return configs
    
    def generate_chat_history(self, output_dir: Path, volume: str):
        """Generate healthcare chat history"""
        print(f" Generating {volume} healthcare chat history...")
        
        conversations = []
        
        if volume == "small":
            conversations = self._generate_small_conversations()
        elif volume == "medium":
            conversations = self._generate_medium_conversations()
        else:  # large
            conversations = self._generate_large_conversations()
        
        # Write to files
        for i, conversation in enumerate(conversations):
            (output_dir / f"healthcare_chat_{i+1}.json").write_text(json.dumps(conversation, indent=2))
        
        print(f" Generated {len(conversations)} chat conversations")
    
    def _generate_small_conversations(self) -> List[Dict[str, Any]]:
        """Generate small set of healthcare conversations"""
        return [
            {
                "user_id": "dr_smith",
                "session_id": self.fake.uuid4(),
                "messages": [
                    {"role": "user", "message": "How do I access patient records securely?"},
                    {"role": "assistant", "message": "To access patient records securely, you need to:\n1. Log in with your credentials\n2. Complete multi-factor authentication\n3. Select the patient from the search\n4. Review the access log\n\nRemember to log out when finished and never share your credentials."},
                    {"role": "user", "message": "What are the HIPAA requirements for patient data?"},
                    {"role": "assistant", "message": "HIPAA requires:\n- Secure storage and transmission\n- Access controls and audit trails\n- Patient consent for data use\n- Regular security assessments\n- Incident response procedures\n- Staff training on privacy practices"}
                ],
                "timestamp": self.fake.date_time_this_month().isoformat(),
                "department": random.choice(self.specialties)
            },
            {
                "user_id": "nurse_jones",
                "session_id": self.fake.uuid4(),
                "messages": [
                    {"role": "user", "message": "I need help with the medical device integration"},
                    {"role": "assistant", "message": "I can help you with medical device integration. What specific device are you working with?"},
                    {"role": "user", "message": "The patient monitor isn't transmitting data"},
                    {"role": "assistant", "message": "For patient monitor connectivity issues:\n1. Check network connection\n2. Verify device configuration\n3. Test data transmission\n4. Contact biomedical engineering if needed\n\nIs the device showing any error messages?"}
                ],
                "timestamp": self.fake.date_time_this_month().isoformat(),
                "department": random.choice(self.specialties)
            }
        ]
    
    def _generate_medium_conversations(self) -> List[Dict[str, Any]]:
        """Generate medium set of healthcare conversations"""
        conversations = self._generate_small_conversations()
        
        # Add more conversations
        for i in range(3):
            conversations.append({
                "user_id": f"healthcare_user_{i+1}",
                "session_id": self.fake.uuid4(),
                "messages": [
                    {"role": "user", "message": f"How do I set up {random.choice(self.focus_areas)}?"},
                    {"role": "assistant", "message": f"Setting up {random.choice(self.focus_areas)} involves several steps. Let me guide you through the process."},
                    {"role": "user", "message": "What are the compliance requirements?"},
                    {"role": "assistant", "message": f"The compliance requirements include {random.choice(self.compliance_standards).upper()} standards and regular audits."},
                    {"role": "user", "message": "Thanks for the help!"},
                    {"role": "assistant", "message": "You're welcome! Feel free to ask if you need any clarification."}
                ],
                "timestamp": self.fake.date_time_this_month().isoformat(),
                "department": random.choice(self.specialties)
            })
        
        return conversations
    
    def _generate_large_conversations(self) -> List[Dict[str, Any]]:
        """Generate large set of healthcare conversations"""
        conversations = self._generate_medium_conversations()
        
        # Add many more conversations
        for i in range(10):
            conversations.append({
                "user_id": f"healthcare_user_{i+10}",
                "session_id": self.fake.uuid4(),
                "messages": [
                    {"role": "user", "message": f"I need help with {random.choice(self.focus_areas)}"},
                    {"role": "assistant", "message": f"I'd be happy to help you with {random.choice(self.focus_areas)}. What specific issue are you facing?"},
                    {"role": "user", "message": f"The system is showing {random.choice(self.compliance_standards)} compliance error"},
                    {"role": "assistant", "message": f"For {random.choice(self.compliance_standards).upper()} compliance issues, here are some steps:\n1. Review current policies\n2. Check system configurations\n3. Verify staff training\n4. Contact compliance team if needed"},
                    {"role": "user", "message": "Can you provide more specific guidance?"},
                    {"role": "assistant", "message": f"Certainly! For {random.choice(self.focus_areas)} issues, you should:\n- Check the documentation\n- Review compliance requirements\n- Test with minimal setup\n- Contact support if needed"}
                ],
                "timestamp": self.fake.date_time_this_month().isoformat(),
                "department": random.choice(self.specialties)
            })
        
        return conversations
