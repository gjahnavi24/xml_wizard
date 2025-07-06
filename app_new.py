"""
XML Wizard - Main Streamlit Application (Refactored)

This is the main entry point for the XML Wizard application, a modular Streamlit 
interface for parsing XSD schemas and generating compliant dummy XML files.

The application now features a clean, modular architecture with separate workflow modules.
"""

import streamlit as st
from config import get_config
from services.file_manager import FileManager
from services.xml_validator import XMLValidator
from services.schema_analyzer import SchemaAnalyzer
from services.xslt_processor import XSLTProcessor
from utils.config_manager import ConfigManager

# Import UI modules
from ui.common_components import (
    apply_custom_css, 
    render_navigation_sidebar, 
    render_workflow_help
)
from ui.agentic_workflow import (
    render_agentic_xslt_workflow, 
    check_agentic_system_availability
)

# TODO: Import other workflow modules when created
# from ui.xsd_workflow import render_xsd_to_xml_workflow
# from ui.xml_transform_workflow import render_xml_transformation_workflow

# Initialize configuration and services
config = get_config()
file_manager = FileManager(config)
xml_validator = XMLValidator(config)
schema_analyzer = SchemaAnalyzer(config)
xslt_processor = XSLTProcessor(config)
config_manager = ConfigManager(config)

# Set page configuration
st.set_page_config(
    page_title=config.ui.default_page_title,
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
apply_custom_css()


def get_available_workflows():
    """Get list of available workflows based on system capabilities."""
    workflows = ["🔧 XSD to XML Generation", "🔄 XML Transformation"]
    
    # Add agentic workflow if available
    if check_agentic_system_availability():
        workflows.append("🤖 Agentic XSLT Analysis")
    
    return workflows


def extract_section_name(workflow: str) -> str:
    """Extract the section name from workflow display string."""
    mapping = {
        "🔧 XSD to XML Generation": "XSD to XML Generation",
        "🔄 XML Transformation": "XML Transformation", 
        "🤖 Agentic XSLT Analysis": "Agentic XSLT Analysis"
    }
    return mapping.get(workflow, workflow)


def render_placeholder_workflow(workflow_name: str):
    """Render a placeholder for workflows not yet refactored."""
    st.markdown(f'<div class="main-header">{workflow_name}</div>', unsafe_allow_html=True)
    st.info(f"🚧 **{workflow_name}** workflow is being refactored into modular components.")
    st.markdown("This workflow will be available in the refactored version soon.")
    
    # Provide a link to the original app
    st.markdown("---")
    st.markdown("### 💡 Alternative Access")
    st.info("You can still access all workflows through the original app.py file until refactoring is complete.")


def main():
    """Main application function."""
    # Initialize navigation state
    if 'current_section' not in st.session_state:
        st.session_state['current_section'] = 'XSD to XML Generation'
    
    # Get available workflows
    available_workflows = get_available_workflows()
    
    # Render navigation sidebar
    selected_workflow = render_navigation_sidebar(
        st.session_state['current_section'], 
        available_workflows
    )
    
    # Update current section
    st.session_state['current_section'] = extract_section_name(selected_workflow)
    
    # Render workflow-specific help
    render_workflow_help(st.session_state['current_section'])
    
    # Main content area
    if st.session_state['current_section'] == 'XSD to XML Generation':
        render_placeholder_workflow("XSD to XML Generation")
        
    elif st.session_state['current_section'] == 'XML Transformation':
        render_placeholder_workflow("XML Transformation")
        
    elif st.session_state['current_section'] == 'Agentic XSLT Analysis':
        if check_agentic_system_availability():
            render_agentic_xslt_workflow()
        else:
            st.error("🚫 Agentic XSLT Analysis system is not available. Please check the agentic_test_gen installation.")
    
    else:
        st.error(f"Unknown workflow: {st.session_state['current_section']}")


if __name__ == "__main__":
    main()