import time
import json
from pathlib import Path

def check_progress():
    """Check analysis progress by counting completed analyses."""
    outputs_dir = Path("automated_analysis_results")
    if not outputs_dir.exists():
        return 0, "No outputs directory yet"
    
    # Count session directories
    session_dirs = list(outputs_dir.glob("session_*"))
    if not session_dirs:
        return 0, "No session directories yet"
    
    # Get the latest session
    latest_session = max(session_dirs, key=lambda p: p.stat().st_mtime)
    
    # Check for session data
    session_data_file = latest_session / "session_data.json"
    if session_data_file.exists():
        with open(session_data_file, 'r') as f:
            data = json.load(f)
            records = data.get('records', [])
            
            # Count unique dilemmas processed
            dilemmas_processed = set()
            frameworks_per_dilemma = {}
            
            for record in records:
                dilemma = record.get('dilemma', '')
                framework = record.get('deictic_framing', '')
                if dilemma:
                    dilemmas_processed.add(dilemma)
                    if dilemma not in frameworks_per_dilemma:
                        frameworks_per_dilemma[dilemma] = set()
                    frameworks_per_dilemma[dilemma].add(framework)
            
            total_analyses = len(records)
            num_dilemmas = len(dilemmas_processed)
            
            # Get current dilemma being processed
            if records:
                current_dilemma = records[-1].get('dilemma', 'Unknown')
                current_framework = records[-1].get('deictic_framing', 'Unknown')
            else:
                current_dilemma = "Starting..."
                current_framework = ""
            
            return total_analyses, f"Processed {num_dilemmas}/10 dilemmas, {total_analyses}/80 total analyses. Current: {current_dilemma} ({current_framework})"
    
    return 0, "Session data not yet available"

if __name__ == "__main__":
    print("🔍 Monitoring analysis progress...")
    print("Press Ctrl+C to stop monitoring\n")
    
    last_count = 0
    while True:
        try:
            count, status = check_progress()
            if count != last_count:
                print(f"[{time.strftime('%H:%M:%S')}] {status}")
                last_count = count
                
                # Check if complete
                if count >= 80:
                    print("\n✅ Analysis complete! All 10 dilemmas processed across 8 frameworks.")
                    break
            
            time.sleep(10)  # Check every 10 seconds
            
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped.")
            break
        except Exception as e:
            print(f"Error checking progress: {e}")
            time.sleep(10)