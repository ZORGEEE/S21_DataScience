from config import num_of_steps, report_template
from analytics import Research, Analytics

def main():
    try:
        research = Research('data.csv')
        data = research.file_reader()
        
        # Compute statistics
        analytics = Analytics(data)
        heads, tails = analytics.counts()
        head_percent, tail_percent = analytics.fractions(heads, tails)
        
        # Generate predictions
        predictions = analytics.predict_random(num_of_steps)
        predicted_heads = sum(1 for pred in predictions if pred == [1, 0])
        predicted_tails = num_of_steps - predicted_heads
        
        # Generate report
        report = report_template.format(
            observations=len(data),
            tails=tails,
            heads=heads,
            tail_percent=tail_percent,
            head_percent=head_percent,
            num_predictions=num_of_steps,
            predicted_tails=predicted_tails,
            predicted_heads=predicted_heads
        )
        
        # Save report
        analytics.save_file(report, 'report', 'txt')
        print("Report generated successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()