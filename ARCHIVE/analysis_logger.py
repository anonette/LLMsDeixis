"""
Rich Analysis Logger: Structured logging for deictic analysis results.
Designed for comprehensive research data collection and analysis.
"""

import json
import csv
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DeicticAnalysisRecord:
    """Structured record for a single deictic analysis."""
    timestamp: str
    session_id: str
    dilemma_id: str
    dilemma_title: str
    dilemma_domain: str
    dilemma_complexity: float
    original_description: str
    framing_type: str
    transformation_prompt: str
    direct_question: str
    extracted_tension: str
    llm_response: Optional[str]
    processing_time: float
    deictic_markers: Dict[str, int]
    suggested_frame: str
    frame_confidence: float
    total_markers: int
    response_length: Optional[int]
    
    # Analysis metadata
    analysis_version: str = "1.0"
    transformer_type: str = "generative"

@dataclass
class ExperimentSession:
    """Metadata for a complete analysis session."""
    session_id: str
    start_time: str
    end_time: Optional[str]
    dilemmas_analyzed: int
    framings_tested: List[str]
    total_analyses: int
    experiment_notes: str
    transformer_config: Dict[str, Any]

class RichAnalysisLogger:
    """
    Comprehensive logging system for deictic analysis research.
    Outputs structured data in multiple formats for easy analysis.
    """
    
    def __init__(self, output_dir: str = "analysis_results"):
        """Initialize the logger with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create session ID
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create session directory
        self.session_dir = self.output_dir
        
        # Initialize data containers
        self.records: List[DeicticAnalysisRecord] = []
        self.session_metadata: Optional[ExperimentSession] = None
        
        # Set up file paths
        self.json_file = self.output_dir / f"deictic_analysis_{self.session_id}.json"
        self.csv_file = self.output_dir / f"deictic_analysis_{self.session_id}.csv"
        self.summary_file = self.output_dir / f"session_summary_{self.session_id}.json"
        
        logger.info(f"Analysis logger initialized - Session: {self.session_id}")
    
    def start_session(self, experiment_notes: str = "", transformer_config: Dict[str, Any] = None):
        """Start a new analysis session."""
        self.session_metadata = ExperimentSession(
            session_id=self.session_id,
            start_time=datetime.now().isoformat(),
            end_time=None,
            dilemmas_analyzed=0,
            framings_tested=[],
            total_analyses=0,
            experiment_notes=experiment_notes,
            transformer_config=transformer_config or {}
        )
        logger.info(f"Started analysis session: {self.session_id}")
    
    def log_analysis(self,
                    dilemma_id: str,
                    dilemma_title: str,
                    dilemma_domain: str,
                    dilemma_complexity: float,
                    original_description: str,
                    framing_type: str,
                    transformation_prompt: str,
                    direct_question: str,
                    extracted_tension: str,
                    deictic_markers: Dict[str, int],
                    suggested_frame: str,
                    frame_confidence: float,
                    processing_time: float,
                    llm_response: Optional[str] = None,
                    extended_analysis: Optional[Dict[str, Any]] = None) -> None:
        """Log a single deictic analysis result."""
        
        record = DeicticAnalysisRecord(
            timestamp=datetime.now().isoformat(),
            session_id=self.session_id,
            dilemma_id=dilemma_id,
            dilemma_title=dilemma_title,
            dilemma_domain=dilemma_domain,
            dilemma_complexity=dilemma_complexity,
            original_description=original_description,
            framing_type=framing_type,
            transformation_prompt=transformation_prompt,
            direct_question=direct_question,
            extracted_tension=extracted_tension,
            llm_response=llm_response,
            processing_time=processing_time,
            deictic_markers=deictic_markers,
            suggested_frame=suggested_frame,
            frame_confidence=frame_confidence,
            total_markers=deictic_markers.get('total_markers', 0),
            response_length=len(llm_response) if llm_response else None
        )
        
        self.records.append(record)
        
        # Update session metadata
        if self.session_metadata:
            self.session_metadata.total_analyses += 1
            if framing_type not in self.session_metadata.framings_tested:
                self.session_metadata.framings_tested.append(framing_type)
        
        logger.debug(f"Logged analysis: {dilemma_id} - {framing_type}")
    
    def end_session(self):
        """End the current session and finalize metadata."""
        if self.session_metadata:
            self.session_metadata.end_time = datetime.now().isoformat()
            self.session_metadata.dilemmas_analyzed = len(set(r.dilemma_id for r in self.records))
        
        logger.info(f"Ended analysis session: {self.session_id}")
    
    def save_results(self, include_responses: bool = True):
        """Save all results to structured files."""
        
        # Prepare data for export
        export_data = []
        for record in self.records:
            record_dict = asdict(record)
            
            # Flatten deictic markers for easier analysis
            markers = record_dict.pop('deictic_markers', {})
            for marker_type, count in markers.items():
                record_dict[f'marker_{marker_type}'] = count
            
            # Optionally exclude large text fields for smaller files
            if not include_responses:
                record_dict.pop('llm_response', None)
                record_dict.pop('original_description', None)
                record_dict.pop('transformation_prompt', None)
            
            export_data.append(record_dict)
        
        # Save as JSON (full structured data)
        full_export = {
            'session_metadata': asdict(self.session_metadata) if self.session_metadata else {},
            'records': [asdict(record) for record in self.records],
            'export_timestamp': datetime.now().isoformat(),
            'total_records': len(self.records)
        }
        
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(full_export, f, indent=2, ensure_ascii=False)
        
        # Save as CSV (flattened for analysis tools)
        if export_data:
            df = pd.DataFrame(export_data)
            df.to_csv(self.csv_file, index=False)
        
        # Save session summary
        if self.session_metadata:
            with open(self.summary_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.session_metadata), f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved:")
        logger.info(f"  JSON: {self.json_file}")
        logger.info(f"  CSV: {self.csv_file}")
        logger.info(f"  Summary: {self.summary_file}")
    
    def generate_analysis_report(self) -> Dict[str, Any]:
        """Generate a comprehensive analysis report."""
        if not self.records:
            return {"error": "No records to analyze"}
        
        # Basic statistics
        total_records = len(self.records)
        unique_dilemmas = len(set(r.dilemma_id for r in self.records))
        unique_framings = len(set(r.framing_type for r in self.records))
        
        # Processing time statistics
        processing_times = [r.processing_time for r in self.records]
        avg_processing_time = sum(processing_times) / len(processing_times)
        
        # Deictic marker analysis
        marker_totals = {}
        for record in self.records:
            for marker_type, count in record.deictic_markers.items():
                if marker_type != 'total_markers':
                    marker_totals[marker_type] = marker_totals.get(marker_type, 0) + count
        
        # Frame confidence analysis
        confidence_by_frame = {}
        for record in self.records:
            frame = record.framing_type
            if frame not in confidence_by_frame:
                confidence_by_frame[frame] = []
            confidence_by_frame[frame].append(record.frame_confidence)
        
        # Average confidence per frame
        avg_confidence_by_frame = {
            frame: sum(confidences) / len(confidences)
            for frame, confidences in confidence_by_frame.items()
        }
        
        # Response length analysis (if available)
        response_lengths = [r.response_length for r in self.records if r.response_length is not None]
        avg_response_length = sum(response_lengths) / len(response_lengths) if response_lengths else 0
        
        report = {
            "session_summary": {
                "session_id": self.session_id,
                "total_analyses": total_records,
                "unique_dilemmas": unique_dilemmas,
                "unique_framings": unique_framings,
                "avg_processing_time": avg_processing_time,
                "avg_response_length": avg_response_length
            },
            "deictic_marker_totals": marker_totals,
            "frame_confidence_analysis": avg_confidence_by_frame,
            "framing_distribution": {
                framing: len([r for r in self.records if r.framing_type == framing])
                for framing in set(r.framing_type for r in self.records)
            },
            "complexity_analysis": {
                "avg_complexity": sum(r.dilemma_complexity for r in self.records) / total_records,
                "complexity_range": [
                    min(r.dilemma_complexity for r in self.records),
                    max(r.dilemma_complexity for r in self.records)
                ]
            }
        }
        
        return report
    
    def save_analysis_report(self):
        """Save the comprehensive analysis report."""
        report = self.generate_analysis_report()
        report_file = self.output_dir / f"analysis_report_{self.session_id}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Analysis report saved: {report_file}")
        return report
    
    def get_records_dataframe(self) -> pd.DataFrame:
        """Get all records as a pandas DataFrame for analysis."""
        if not self.records:
            return pd.DataFrame()
        
        # Convert records to flat dictionaries
        flat_records = []
        for record in self.records:
            flat_record = asdict(record)
            
            # Flatten deictic markers
            markers = flat_record.pop('deictic_markers', {})
            for marker_type, count in markers.items():
                flat_record[f'marker_{marker_type}'] = count
            
            flat_records.append(flat_record)
        
        return pd.DataFrame(flat_records)
    
    def export_for_statistical_analysis(self, statistical_package: str = "r"):
        """Export data in formats suitable for statistical analysis."""
        df = self.get_records_dataframe()
        
        if statistical_package.lower() == "r":
            # R-friendly CSV with proper encoding
            r_file = self.output_dir / f"for_R_analysis_{self.session_id}.csv"
            df.to_csv(r_file, index=False, encoding='utf-8')
            logger.info(f"R analysis file saved: {r_file}")
        
        elif statistical_package.lower() == "spss":
            # SPSS-friendly format
            spss_file = self.output_dir / f"for_SPSS_analysis_{self.session_id}.sav"
            try:
                df.to_spss(spss_file)
                logger.info(f"SPSS analysis file saved: {spss_file}")
            except ImportError:
                logger.warning("pyreadstat not available for SPSS export")
        
        elif statistical_package.lower() == "python":
            # Python pickle for easy loading
            pickle_file = self.output_dir / f"for_python_analysis_{self.session_id}.pkl"
            df.to_pickle(pickle_file)
            logger.info(f"Python pickle file saved: {pickle_file}")
    
    def print_session_summary(self):
        """Print a formatted summary of the current session."""
        if not self.records:
            print("No analysis records found.")
            return
        
        report = self.generate_analysis_report()
        
        print("\n" + "="*60)
        print("DEICTIC ANALYSIS SESSION SUMMARY")
        print("="*60)
        
        summary = report["session_summary"]
        print(f"Session ID: {summary['session_id']}")
        print(f"Total Analyses: {summary['total_analyses']}")
        print(f"Unique Dilemmas: {summary['unique_dilemmas']}")
        print(f"Unique Framings: {summary['unique_framings']}")
        print(f"Avg Processing Time: {summary['avg_processing_time']:.3f}s")
        print(f"Avg Response Length: {summary['avg_response_length']:.0f} chars")
        
        print(f"\nFraming Distribution:")
        for framing, count in report["framing_distribution"].items():
            print(f"  {framing}: {count}")
        
        print(f"\nTop Deictic Markers:")
        sorted_markers = sorted(report["deictic_marker_totals"].items(), 
                              key=lambda x: x[1], reverse=True)[:5]
        for marker, count in sorted_markers:
            print(f"  {marker}: {count}")
        
        print(f"\nFrame Confidence (avg):")
        for frame, confidence in report["frame_confidence_analysis"].items():
            print(f"  {frame}: {confidence:.3f}")
        
        print("="*60)
