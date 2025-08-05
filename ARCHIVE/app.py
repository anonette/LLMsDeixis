"""
Streamlit Web Interface for Deictic Research System
Interactive web app for analyzing ethical reasoning in LLMs
"""

import streamlit as st
import asyncio
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import analysis components
from deixis_ethical_analyzer import DeicticEthicalAnalyzer, EthicalDilemmaDatabase
from critical_expert_analysis import CriticalExpertAnalyzer
from evidence_based_expert_analysis import EvidenceBasedExpertAnalyzer
from models.schemas import DeicticFraming

# Page configuration
st.set_page_config(
    page_title="Deixis Machines - Deictic Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def check_api_keys():
    """Check if API keys are configured."""
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not openrouter_key:
        st.error("❌ OPENROUTER_API_KEY not found in .env file")
        st.info("Please add your OpenRouter API key to the .env file")
        return False
    return True

def load_results_data():
    """Load available analysis results."""
    results_dir = Path("automated_analysis_results")
    if not results_dir.exists():
        return []
    
    sessions = []
    for session_path in results_dir.glob("session_*"):
        if session_path.is_dir():
            readme_file = session_path / "README_RESULTS.json"
            if readme_file.exists():
                try:
                    with open(readme_file, 'r') as f:
                        session_info = json.load(f)
                    session_info['path'] = session_path
                    sessions.append(session_info)
                except Exception as e:
                    st.error(f"Error loading session {session_path.name}: {e}")
    
    return sorted(sessions, key=lambda x: x['session_info']['timestamp'], reverse=True)

def display_dilemma_preview():
    """Display preview of available ethical dilemmas."""
    st.header("📋 Available Ethical Dilemmas")
    
    db = EthicalDilemmaDatabase()
    dilemmas = db.get_all_dilemmas()
    
    for i, dilemma in enumerate(dilemmas):
        with st.expander(f"{i+1}. {dilemma.title} (Complexity: {dilemma.complexity_score}/10)"):
            st.write(f"**Domain:** {dilemma.domain}")
            st.write(f"**Description:** {dilemma.description}")
            st.write(f"**Tags:** {', '.join(dilemma.tags)}")

def display_framework_overview():
    """Display the 8 deictic frameworks."""
    st.header("🎯 Deictic Frameworks")
    
    frameworks = {
        "Impersonal": "Objective, neutral perspective removing personal agency",
        "Second Person": "Direct address making 'you' the decision-maker",
        "First Person": "Personal 'I' perspective as the decision-maker",
        "Reflexive": "Perspective-taking and role reversal",
        "Dialogic": "Collective 'we' decision-making",
        "Spatial": "Physical positioning and embodied perspective",
        "Temporal": "Time urgency and critical moments",
        "Cosmological": "Universal, spiritual, cosmic perspective"
    }
    
    cols = st.columns(2)
    for i, (name, description) in enumerate(frameworks.items()):
        col = cols[i % 2]
        with col:
            st.info(f"**{name}**: {description}")

def run_automated_analysis():
    """Run the automated analysis."""
    if not check_api_keys():
        return
    
    st.header("🚀 Automated Analysis")
    
    st.info("""
    This will run a complete analysis of all 5 ethical dilemmas across all 8 deictic frameworks.
    
    **What it does:**
    - Analyzes 5 dilemmas × 8 frameworks = 40 total analyses
    - Generates comparative reports
    - Runs critical expert analysis
    - Produces evidence-based insights
    - Creates visualizations and summaries
    
    **Time required:** 10-20 minutes depending on API response times
    """)
    
    if st.button("🎯 Start Automated Analysis", type="primary"):
        with st.spinner("Running automated analysis... This will take several minutes."):
            try:
                # Import and run the automated analysis
                from run_analysis import run_full_automated_analysis
                
                # Create a progress placeholder
                progress_placeholder = st.empty()
                status_placeholder = st.empty()
                
                progress_placeholder.progress(0)
                status_placeholder.info("🔧 Initializing analyzers...")
                
                # Run analysis (this is a simplified version for demo)
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    loop.run_until_complete(run_full_automated_analysis())
                    st.success("✅ Analysis completed successfully!")
                    st.info("Check the 'View Results' tab to explore your results.")
                    st.rerun()
                finally:
                    loop.close()
                    
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.info("Please check your API keys and internet connection.")

def display_analysis_results():
    """Display analysis results."""
    st.header("📊 Analysis Results")
    
    sessions = load_results_data()
    
    if not sessions:
        st.info("No analysis results found. Run an automated analysis first.")
        return
    
    # Session selector
    session_names = [f"Session {s['session_info']['timestamp']} ({s['session_info']['total_dilemmas_analyzed']} dilemmas)" for s in sessions]
    selected_idx = st.selectbox("Select Analysis Session:", range(len(session_names)), format_func=lambda x: session_names[x])
    
    if selected_idx is not None:
        session = sessions[selected_idx]
        session_path = session['path']
        
        # Display session info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Dilemmas Analyzed", session['session_info']['total_dilemmas_analyzed'])
        with col2:
            st.metric("Framework Analyses", session['session_info']['total_framework_analyses'])
        with col3:
            st.metric("Timestamp", session['session_info']['timestamp'])
        
        # Tabs for different result types
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Comparative Analysis", "🔍 Critical Insights", "📋 Evidence-Based", "💾 Raw Data"])
        
        with tab1:
            display_comparative_results(session_path)
        
        with tab2:
            display_critical_results(session_path)
        
        with tab3:
            display_evidence_results(session_path)
        
        with tab4:
            display_raw_data(session_path)

def display_comparative_results(session_path):
    """Display comparative analysis results."""
    comparative_file = session_path / "comparative_reports.json"
    
    # Check what files actually exist in the session directory
    with st.expander("🔍 Debug: Available Files in Session"):
        json_files = list(session_path.glob("*.json"))
        if json_files:
            st.write("**Found JSON files:**")
            for file in json_files:
                st.write(f"• {file.name} ({file.stat().st_size} bytes)")
        else:
            st.write("❌ No JSON files found in session directory")
        
        # Also check for any analysis files
        all_files = list(session_path.iterdir())
        st.write(f"**Total files in session:** {len(all_files)}")
    
    if not comparative_file.exists():
        st.warning("⚠️ comparative_reports.json not found. Trying to load raw analysis data...")
        
        # Try to load from raw analysis results instead
        raw_file = session_path / "raw_analysis_results.json"
        session_data_file = session_path / "session_data.json"
        
        if raw_file.exists():
            try:
                with open(raw_file, 'r') as f:
                    raw_data = json.load(f)
                st.info(f"✅ Found raw_analysis_results.json with {len(raw_data)} entries")
                
                # Display raw data structure for debugging
                with st.expander("📊 Raw Data Structure Preview"):
                    if raw_data:
                        first_key = list(raw_data.keys())[0]
                        st.write(f"**Sample entry key:** {first_key}")
                        if isinstance(raw_data[first_key], dict):
                            st.write("**Sample entry structure:**")
                            for key in list(raw_data[first_key].keys())[:10]:  # Show first 10 keys
                                st.write(f"• {key}")
                
                # Try to create basic visualizations from raw data
                display_raw_data_analysis(raw_data)
                return
                
            except Exception as e:
                st.error(f"Error loading raw data: {e}")
        
        elif session_data_file.exists():
            try:
                with open(session_data_file, 'r') as f:
                    session_data = json.load(f)
                st.info(f"✅ Found session_data.json")
                
                # Display session data structure
                with st.expander("📊 Session Data Structure Preview"):
                    if 'records' in session_data:
                        st.write(f"**Records found:** {len(session_data['records'])}")
                        if session_data['records']:
                            sample_record = session_data['records'][0]
                            st.write("**Sample record keys:**")
                            for key in sample_record.keys():
                                st.write(f"• {key}")
                
                # Try to create visualizations from session data
                display_session_data_analysis(session_data)
                return
                
            except Exception as e:
                st.error(f"Error loading session data: {e}")
        
        st.error("❌ No usable analysis data found. Please run the analysis first or use the Continue Analysis tab to complete the analysis.")
        return
    
    try:
        with open(comparative_file, 'r') as f:
            reports = json.load(f)
        
        st.subheader("Cross-Framework Comparison")
        
        if not reports:
            st.warning("No comparative reports found in the file.")
            return
        
        st.info(f"Found {len(reports)} dilemma analyses")
        
        for dilemma_id, report in reports.items():
            with st.expander(f"Analysis: {dilemma_id}"):
                
                # Debug: Show what keys are in this report
                st.write(f"**Available data sections:** {list(report.keys())}")
                
                # Agency patterns visualization
                if 'agency_patterns' in report:
                    st.write("**Agency Distribution Patterns:**")
                    
                    agency_data = []
                    for framework, data in report['agency_patterns'].items():
                        agency_data.append({
                            'Framework': framework,
                            'Collective vs Individual': data.get('collective_vs_individual', 0),
                            'Primary Agent': data.get('primary_agent', 'Unknown')
                        })
                    
                    if agency_data:
                        df = pd.DataFrame(agency_data)
                        fig = px.bar(df, x='Framework', y='Collective vs Individual', 
                                   title="Agency Distribution by Framework")
                        st.plotly_chart(fig, use_container_width=True, key=f"agency_{dilemma_id}")
                    else:
                        st.write("No agency pattern data available")
                else:
                    st.write("❌ No agency_patterns section found")
                
                # Ethical patterns
                if 'ethical_patterns' in report:
                    st.write("**Ethical Reasoning Patterns:**")
                    
                    ethical_data = []
                    for framework, data in report['ethical_patterns'].items():
                        ethical_data.append({
                            'Framework': framework,
                            'Consequence vs Duty': data.get('consequence_vs_duty', 0),
                            'Reasoning Type': data.get('reasoning_type', 'Unknown')
                        })
                    
                    if ethical_data:
                        df = pd.DataFrame(ethical_data)
                        fig = px.scatter(df, x='Framework', y='Consequence vs Duty',
                                       size_max=60, title="Ethical Reasoning Orientation")
                        st.plotly_chart(fig, use_container_width=True, key=f"ethical_{dilemma_id}")
                    else:
                        st.write("No ethical pattern data available")
                else:
                    st.write("❌ No ethical_patterns section found")
                
                # Response statistics
                if 'response_statistics' in report:
                    stats = report['response_statistics']
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Average Response Length", f"{stats.get('avg_length', 0):.0f} chars")
                    with col2:
                        st.metric("Total Processing Time", f"{stats.get('total_processing_time', 0):.1f}s")
                else:
                    st.write("❌ No response_statistics section found")
                
    except Exception as e:
        st.error(f"Error loading comparative results: {e}")
        st.write("**Exception details:**", str(e))

def display_raw_data_analysis(raw_data):
    """Create basic analysis from raw data when comparative reports aren't available."""
    st.subheader("📊 Basic Analysis from Raw Data")
    
    # Group by dilemma and framework
    frameworks = set()
    dilemmas = set()
    
    for key in raw_data.keys():
        if '_' in key:
            parts = key.split('_')
            if len(parts) >= 2:
                dilemma = '_'.join(parts[:-1])
                framework = parts[-1]
                dilemmas.add(dilemma)
                frameworks.add(framework)
    
    st.write(f"**Found {len(dilemmas)} dilemmas and {len(frameworks)} frameworks**")
    
    # Create simple response length comparison
    response_lengths = []
    for key, data in raw_data.items():
        if isinstance(data, dict) and 'llm_response' in data:
            response_len = len(data['llm_response'])
            if '_' in key:
                parts = key.split('_')
                framework = parts[-1]
                response_lengths.append({
                    'Framework': framework,
                    'Response Length': response_len,
                    'Key': key
                })
    
    if response_lengths:
        df = pd.DataFrame(response_lengths)
        fig = px.box(df, x='Framework', y='Response Length', 
                     title="Response Length Distribution by Framework")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("❌ Could not extract response length data")

def display_session_data_analysis(session_data):
    """Create basic analysis from session data when comparative reports aren't available."""
    st.subheader("📊 Analysis from Session Data")
    
    if 'records' not in session_data:
        st.error("No 'records' found in session data")
        return
    
    records = session_data['records']
    if not records:
        st.error("Records list is empty")
        return
    
    # Extract data for visualization
    analysis_data = []
    for record in records:
        if isinstance(record, dict):
            framework = record.get('deictic_framing', 'unknown')
            dilemma = record.get('dilemma_id', 'unknown')
            response_length = len(record.get('llm_response', ''))
            processing_time = record.get('processing_time', 0)
            
            analysis_data.append({
                'Framework': framework,
                'Dilemma': dilemma,
                'Response Length': response_length,
                'Processing Time': processing_time
            })
    
    if analysis_data:
        df = pd.DataFrame(analysis_data)
        
        # Response length by framework
        fig1 = px.box(df, x='Framework', y='Response Length',
                      title="Response Length by Deictic Framework")
        fig1.update_xaxes(tickangle=45)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Processing time by framework
        fig2 = px.box(df, x='Framework', y='Processing Time',
                      title="Processing Time by Deictic Framework")
        fig2.update_xaxes(tickangle=45)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Summary statistics
        st.write("**Summary Statistics:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Avg Response Length", f"{df['Response Length'].mean():.0f} chars")
        with col3:
            st.metric("Avg Processing Time", f"{df['Processing Time'].mean():.1f}s")
    else:
        st.error("Could not extract analysis data from records")

def display_critical_results(session_path):
    """Display critical analysis results."""
    critical_file = session_path / "critical_analysis.json"
    
    if not critical_file.exists():
        st.warning("Critical analysis data not found.")
        return
    
    try:
        with open(critical_file, 'r') as f:
            insights = json.load(f)
        
        st.subheader("Critical Research Insights")
        
        for rq_id, rq_insights in insights.items():
            with st.expander(f"Research Question {rq_id}"):
                for insight in rq_insights:
                    st.write(f"**Insight:** {insight['insight_statement']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Confidence Level", f"{insight['confidence_level']:.2f}")
                    
                    st.write("**✅ What Works:**")
                    for item in insight['what_works']:
                        st.write(f"• {item}")
                    
                    st.write("**❌ What Doesn't Work:**")
                    for item in insight['what_doesnt_work']:
                        st.write(f"• {item}")
                    
                    st.write("**🤔 Challenging Questions:**")
                    for item in insight['challenging_questions'][:3]:
                        st.write(f"• {item}")
                    
    except Exception as e:
        st.error(f"Error loading critical results: {e}")

def display_evidence_results(session_path):
    """Display evidence-based analysis results."""
    evidence_file = session_path / "evidence_based_analysis.json"
    
    if not evidence_file.exists():
        st.warning("Evidence-based analysis data not found.")
        return
    
    try:
        with open(evidence_file, 'r') as f:
            insights = json.load(f)
        
        st.subheader("Evidence-Based Research Insights")
        
        for rq_id, rq_insights in insights.items():
            with st.expander(f"Research Question {rq_id}"):
                for insight in rq_insights:
                    st.write(f"**Insight:** {insight['insight_statement']}")
                    st.metric("Confidence Level", f"{insight['confidence_level']:.2f}")
                    
                    st.write("**🔍 Concrete Examples:**")
                    for example in insight['concrete_examples']:
                        st.write(f"• {example}")
                    
                    st.write("**📈 Quantitative Support:**")
                    for key, value in insight['quantitative_support'].items():
                        st.write(f"• {key}: {value}")
                    
                    st.write("**⚠️ Acknowledged Limitations:**")
                    for limitation in insight['limitations_acknowledged']:
                        st.write(f"• {limitation}")
                    
    except Exception as e:
        st.error(f"Error loading evidence results: {e}")

def display_raw_data(session_path):
    """Display raw data files."""
    st.subheader("Raw Data Files")
    
    files = [
        ("raw_analysis_results.json", "Complete analysis data with all responses"),
        ("session_data.json", "Rich logging data with detailed metrics"),
        ("analysis_report.json", "Comprehensive analysis report"),
        ("README_RESULTS.json", "Session summary and file descriptions")
    ]
    
    for filename, description in files:
        file_path = session_path / filename
        if file_path.exists():
            with st.expander(f"📄 {filename}"):
                st.write(description)
                st.write(f"**File size:** {file_path.stat().st_size / 1024:.1f} KB")
                
                if st.button(f"Download {filename}", key=filename):
                    with open(file_path, 'r') as f:
                        st.download_button(
                            label=f"💾 Download {filename}",
                            data=f.read(),
                            file_name=filename,
                            mime="application/json"
                        )

def main():
    """Main Streamlit app."""
    st.title("🔬 Deixis Machines - Deictic Research System")
    st.markdown("*Exploring how linguistic structure shapes moral reasoning in LLMs*")
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio("Go to:", [
            "🏠 Home",
            "📋 Dilemmas & Frameworks", 
            "🚀 Run Analysis",
            "📊 View Results",
            "🔄 Continue Analysis"
        ])
        
        st.markdown("---")
        st.markdown("### System Status")
        
        if check_api_keys():
            st.success("✅ API Keys Configured")
        else:
            st.error("❌ API Keys Missing")
        
        # Results count
        sessions = load_results_data()
        st.info(f"📊 {len(sessions)} analysis sessions available")
    
    # Main content
    if page == "🏠 Home":
        st.header("Welcome to Deixis Machines")
        
        st.markdown("""
        ### 🎯 Research Objective
        This system analyzes how deictic (context-dependent) linguistic structures influence 
        ethical reasoning and agency attribution in Large Language Models.
        
        ### 🔬 Methodology
        - **Zero Hardcoding**: All analysis generated by LLMs themselves
        - **8 Deictic Frameworks**: Different linguistic perspectives on ethical dilemmas
        - **5 Realistic Dilemmas**: Contemporary ethical conflicts people actually face
        - **Critical Analysis**: Rigorous evaluation of findings and limitations
        
        ### 🚀 Getting Started
        1. **View Dilemmas & Frameworks** - Explore the ethical scenarios and linguistic approaches
        2. **Run Analysis** - Execute automated analysis across all frameworks
        3. **View Results** - Examine findings, visualizations, and insights
        
        ### 📊 What You'll Get
        - Comparative analysis across deictic frameworks
        - Critical research insights with uncertainty quantification
        - Evidence-based findings with concrete examples
        - Publication-ready data and visualizations
        """)
        
    elif page == "📋 Dilemmas & Frameworks":
        display_dilemma_preview()
        st.markdown("---")
        display_framework_overview()
        
    elif page == "🚀 Run Analysis":
        run_automated_analysis()
        
    elif page == "📊 View Results":
        display_analysis_results()
        
    elif page == "🔄 Continue Analysis":
        continue_existing_analysis()

def continue_existing_analysis():
    """Continue analysis from existing incomplete session."""
    st.header("🔄 Continue Analysis from Existing Session")
    
    # Find incomplete sessions
    results_dir = Path("automated_analysis_results")
    if not results_dir.exists():
        st.warning("No analysis results directory found. Please run an analysis first.")
        return
    
    sessions = list(results_dir.glob("session_*"))
    sessions.sort(key=lambda x: x.name, reverse=True)
    
    if not sessions:
        st.warning("No analysis sessions found. Please run an analysis first.")
        return
    
    st.info("""
    This page helps you complete analysis sessions that were interrupted or failed during 
    the critical analysis or markdown generation phase.
    
    **What it does:**
    - Finds your existing session data
    - Generates missing critical expert analysis
    - Creates evidence-based insights 
    - Produces publication-ready markdown reports
    - Shows you the data visually
    """)
    
    # Session selector
    session_options = []
    session_details = []
    
    for session_path in sessions[:5]:  # Show last 5 sessions
        session_name = session_path.name
        
        # Check what files exist
        has_session_data = (session_path / "session_data.json").exists() or any(session_path.glob("deictic_analysis_*.json"))
        has_critical = (session_path / "critical_analysis.json").exists()
        has_evidence = (session_path / "evidence_based_analysis.json").exists()
        has_markdown = (session_path / "README.md").exists()
        
        # Count JSON files to estimate completion
        json_files = list(session_path.glob("*.json"))
        
        status = "✅ Complete" if (has_critical and has_evidence and has_markdown) else "🔄 Incomplete"
        
        session_options.append(f"{session_name} - {status} ({len(json_files)} files)")
        session_details.append({
            'path': session_path,
            'name': session_name,
            'has_session_data': has_session_data,
            'has_critical': has_critical,
            'has_evidence': has_evidence,
            'has_markdown': has_markdown,
            'file_count': len(json_files)
        })
    
    if not session_options:
        st.warning("No sessions found to continue.")
        return
    
    selected_idx = st.selectbox("Select Session to Continue:", range(len(session_options)), 
                               format_func=lambda x: session_options[x])
    
    if selected_idx is not None:
        session_detail = session_details[selected_idx]
        session_path = session_detail['path']
        
        # Display session status
        st.subheader(f"Session: {session_detail['name']}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Session Data", "✅" if session_detail['has_session_data'] else "❌")
        with col2:
            st.metric("Critical Analysis", "✅" if session_detail['has_critical'] else "❌")
        with col3:
            st.metric("Evidence Analysis", "✅" if session_detail['has_evidence'] else "❌")
        with col4:
            st.metric("Markdown Reports", "✅" if session_detail['has_markdown'] else "❌")
        
        # Show what needs to be completed
        missing_items = []
        if not session_detail['has_critical']:
            missing_items.append("Critical Expert Analysis")
        if not session_detail['has_evidence']:
            missing_items.append("Evidence-Based Analysis")
        if not session_detail['has_markdown']:
            missing_items.append("Markdown Reports")
        
        if missing_items:
            st.warning(f"Missing: {', '.join(missing_items)}")
        else:
            st.success("✅ This session appears complete!")
        
        # Preview existing data
        with st.expander("📊 Preview Existing Session Data"):
            try:
                # Try to load session data and calculate actual metrics
                session_data = None
                metrics = {'total_analyses': 40, 'avg_processing_time': 0, 'avg_response_length': 0}
                
                # Try session_data.json first
                session_data_file = session_path / "session_data.json"
                if session_data_file.exists():
                    with open(session_data_file, 'r') as f:
                        session_data = json.load(f)
                
                # Try alternative session files
                if not session_data:
                    alt_files = list(session_path.glob("deictic_analysis_*.json"))
                    if alt_files:
                        with open(alt_files[0], 'r') as f:
                            session_data = json.load(f)
                
                # Try session summary files
                summary_files = list(session_path.glob("session_summary_*.json"))
                if summary_files:
                    with open(summary_files[0], 'r') as f:
                        summary = json.load(f)
                    metrics.update({
                        'total_analyses': summary.get('total_analyses', 40),
                        'avg_processing_time': summary.get('avg_processing_time', 0),
                        'avg_response_length': summary.get('avg_response_length', 0),
                    })
                
                # If we have session_data, calculate from raw records
                if session_data and 'records' in session_data and session_data['records']:
                    records = session_data['records']
                    
                    # Extract processing times and response lengths
                    processing_times = []
                    response_lengths = []
                    
                    for record in records:
                        if isinstance(record, dict):
                            # Try different possible field names
                            proc_time = record.get('processing_time') or record.get('duration') or record.get('elapsed_time', 0)
                            if proc_time:
                                processing_times.append(float(proc_time))
                            
                            # Try different response field names
                            response = record.get('llm_response') or record.get('response') or record.get('output', '')
                            if response:
                                response_lengths.append(len(str(response)))
                    
                    # Calculate averages if we have data
                    if processing_times:
                        metrics['avg_processing_time'] = sum(processing_times) / len(processing_times)
                    if response_lengths:
                        metrics['avg_response_length'] = sum(response_lengths) / len(response_lengths)
                    
                    metrics['total_analyses'] = len(records)
                
                st.write("**Session Summary:**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Analyses", metrics['total_analyses'])
                with col2:
                    st.metric("Avg Processing Time", f"{metrics['avg_processing_time']:.1f}s")
                with col3:
                    st.metric("Avg Response Length", f"{metrics['avg_response_length']:.0f} chars")
                    
                    # Show framing distribution
                    if 'framing_distribution' in summary:
                        st.write("**Framework Distribution:**")
                        framing_data = []
                        for framework, count in summary['framing_distribution'].items():
                            framing_data.append({'Framework': framework, 'Count': count})
                        
                        if framing_data:
                            df = pd.DataFrame(framing_data)
                            fig = px.bar(df, x='Framework', y='Count', title="Analysis Count by Framework")
                            st.plotly_chart(fig, use_container_width=True)
                    
                    # Show top deictic markers
                    if 'top_deictic_markers' in summary:
                        st.write("**Top Deictic Markers:**")
                        markers_data = []
                        for marker, count in list(summary['top_deictic_markers'].items())[:10]:
                            markers_data.append({'Marker': marker, 'Count': count})
                        
                        if markers_data:
                            df = pd.DataFrame(markers_data)
                            fig = px.bar(df, x='Marker', y='Count', title="Most Frequent Deictic Markers")
                            fig.update_xaxes(tickangle=45)
                            st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.warning(f"Could not load session preview: {e}")
        
        # Continue analysis button
        if st.button("🚀 Continue Analysis", type="primary", disabled=not session_detail['has_session_data']):
            if not session_detail['has_session_data']:
                st.error("Cannot continue - no session data found!")
                return
            
            with st.spinner("Completing analysis... This may take a few minutes."):
                try:
                    # Import continuation functions
                    from continue_analysis import load_session_data, load_comparative_reports, generate_missing_analyses, generate_markdown_reports_fixed
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Load session data
                    status_text.text("📄 Loading session data...")
                    progress_bar.progress(20)
                    
                    session_data = load_session_data(session_path)
                    if not session_data:
                        st.error("Failed to load session data!")
                        return
                    
                    # Load comparative reports
                    status_text.text("📊 Loading comparative reports...")
                    progress_bar.progress(40)
                    
                    reports = load_comparative_reports(session_path)
                    
                    # Generate missing analyses
                    status_text.text("🔍 Generating critical and evidence-based analyses...")
                    progress_bar.progress(60)
                    
                    critical_insights, evidence_insights = generate_missing_analyses(session_path, session_data)
                    
                    # Generate markdown reports
                    status_text.text("📝 Generating markdown reports...")
                    progress_bar.progress(80)
                    
                    md_files = generate_markdown_reports_fixed(session_path, reports, critical_insights, evidence_insights)
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Analysis continuation complete!")
                    
                    st.success("🎉 Analysis completed successfully!")
                    
                    # Show what was generated
                    st.write("**Generated Files:**")
                    for filename, description in md_files.items():
                        st.write(f"• **{filename}** - {description}")
                    
                    # Show some results
                    if critical_insights:
                        st.subheader("🔍 Sample Critical Insights")
                        for rq_id, insights in list(critical_insights.items())[:2]:
                            if insights:
                                with st.expander(f"Research Question {rq_id}"):
                                    insight = insights[0]
                                    st.write(f"**Finding:** {insight.get('insight_statement', 'No statement')}")
                                    st.metric("Confidence", f"{insight.get('confidence_level', 0):.2f}")
                                    
                                    if insight.get('what_works'):
                                        st.write("**✅ What Works:**")
                                        for item in insight['what_works'][:3]:
                                            st.write(f"• {item}")
                    
                    if evidence_insights:
                        st.subheader("📊 Sample Evidence-Based Findings")
                        for rq_id, insights in list(evidence_insights.items())[:2]:
                            if insights:
                                with st.expander(f"Research Question {rq_id}"):
                                    insight = insights[0]
                                    st.write(f"**Finding:** {insight.get('insight_statement', 'No statement')}")
                                    
                                    if insight.get('concrete_examples'):
                                        st.write("**🔍 Examples:**")
                                        for example in insight['concrete_examples'][:2]:
                                            st.write(f"• {example}")
                    
                    st.info("💡 Go to the 'View Results' tab to see the complete analysis with all visualizations!")
                    
                except Exception as e:
                    st.error(f"❌ Analysis continuation failed: {str(e)}")
                    st.info("You can try running `python continue_analysis.py` from the command line as an alternative.")

if __name__ == "__main__":
    main()
