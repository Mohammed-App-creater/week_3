"""
Segment Analysis and Reporting for ACIS Insurance Risk Analytics

This module generates comprehensive segment analysis including:
- Segment counts and distribution
- Loss ratio by segment
- Claims distribution per segment
- Average premium per segment
- Geographic risk comparison
- Visualizations (loss ratio chart, segment distribution, premium heatmap)

Author: Data Science Team - ACIS Risk Analytics Project
Date: December 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')


class SegmentReporter:
    """Generate comprehensive segment analysis and visualizations"""
    
    def __init__(self, output_dir='outputs/segments'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set visualization style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['font.size'] = 10
    
    def load_data(self, file_path):
        """Load processed data from parquet file"""
        print(f"Loading data from {file_path}...")
        df = pd.read_parquet(file_path)
        print(f"  Loaded {len(df):,} rows × {len(df.columns)} columns")
        return df
    
    def calculate_segment_counts(self, df):
        """Calculate customer counts per segment"""
        print("\nCalculating segment counts...")
        
        segment_counts = df['RiskSegment'].value_counts().sort_index()
        segment_pct = (segment_counts / len(df) * 100).round(1)
        
        summary = pd.DataFrame({
            'Segment': segment_counts.index,
            'Count': segment_counts.values,
            'Percentage': segment_pct.values
        })
        
        print("\nSegment Distribution:")
        print(summary.to_string(index=False))
        
        return summary
    
    def calculate_loss_ratio_by_segment(self, df):
        """Calculate loss ratios by segment"""
        print("\nCalculating loss ratio by segment...")
        
        segment_metrics = df.groupby('RiskSegment').agg({
            'TotalClaims': 'sum',
            'TotalPremium': 'sum',
            'PolicyID': 'nunique'
        }).reset_index()
        
        segment_metrics['LossRatio'] = (
            segment_metrics['TotalClaims'] / segment_metrics['TotalPremium']
        ).round(3)
        
        segment_metrics['AvgClaimsPerPolicy'] = (
            segment_metrics['TotalClaims'] / segment_metrics['PolicyID']
        ).round(2)
        
        segment_metrics['AvgPremiumPerPolicy'] = (
            segment_metrics['TotalPremium'] / segment_metrics['PolicyID']
        ).round(2)
        
        segment_metrics.columns = [
            'Segment', 'TotalClaims', 'TotalPremium', 'NumPolicies',
            'LossRatio', 'AvgClaimsPerPolicy', 'AvgPremiumPerPolicy'
        ]
        
        print("\nLoss Ratio by Segment:")
        print(segment_metrics.to_string(index=False))
        
        return segment_metrics
    
    def calculate_claims_distribution(self, df):
        """Calculate claims frequency and severity by segment"""
        print("\nCalculating claims distribution by segment...")
        
        claims_dist = df.groupby('RiskSegment').agg({
            'ClaimFrequency': 'mean',
            'ClaimSeverity': 'mean',
            'TotalClaims': ['count', 'sum', 'mean', 'median']
        }).reset_index()
        
        claims_dist.columns = [
            'Segment', 'ClaimFrequency', 'AvgClaimSeverity',
            'NumRecords', 'TotalClaims', 'AvgClaims', 'MedianClaims'
        ]
        
        claims_dist['ClaimFrequency'] = (claims_dist['ClaimFrequency'] * 100).round(1)
        claims_dist['AvgClaimSeverity'] = claims_dist['AvgClaimSeverity'].round(2)
        claims_dist['AvgClaims'] = claims_dist['AvgClaims'].round(2)
        claims_dist['MedianClaims'] = claims_dist['MedianClaims'].round(2)
        
        print("\nClaims Distribution by Segment:")
        print(claims_dist.to_string(index=False))
        
        return claims_dist
    
    def calculate_average_premium(self, df):
        """Calculate average premium by segment"""
        print("\nCalculating average premium by segment...")
        
        premium_stats = df.groupby('RiskSegment')['TotalPremium'].agg([
            'count', 'mean', 'median', 'std', 'min', 'max'
        ]).reset_index()
        
        premium_stats.columns = [
            'Segment', 'Count', 'Mean', 'Median', 'StdDev', 'Min', 'Max'
        ]
        
        for col in ['Mean', 'Median', 'StdDev', 'Min', 'Max']:
            premium_stats[col] = premium_stats[col].round(2)
        
        print("\nPremium Statistics by Segment:")
        print(premium_stats.to_string(index=False))
        
        return premium_stats
    
    def compare_geographic_risk(self, df):
        """Compare risk across provinces and segments"""
        print("\nComparing geographic risk...")
        
        if 'Province' not in df.columns:
            print("  Province column not found, skipping geographic analysis")
            return None
        
        geo_risk = df.groupby(['Province', 'RiskSegment']).agg({
            'TotalClaims': 'sum',
            'TotalPremium': 'sum',
            'PolicyID': 'nunique'
        }).reset_index()
        
        geo_risk['LossRatio'] = (
            geo_risk['TotalClaims'] / geo_risk['TotalPremium']
        ).round(3)
        
        geo_risk['AvgPremium'] = (
            geo_risk['TotalPremium'] / geo_risk['PolicyID']
        ).round(2)
        
        print("\nGeographic Risk by Province and Segment:")
        print(geo_risk.head(15).to_string(index=False))
        
        return geo_risk
    
    def plot_loss_ratio_by_segment(self, segment_metrics):
        """Create bar chart of loss ratios by segment"""
        print("\nCreating loss ratio by segment plot...")
        
        plt.figure(figsize=(10, 6))
        
        colors = {'Low-Risk': '#2ecc71', 'Medium-Risk': '#f39c12', 'High-Risk': '#e74c3c'}
        segment_colors = [colors.get(seg, '#95a5a6') for seg in segment_metrics['Segment']]
        
        bars = plt.bar(segment_metrics['Segment'], segment_metrics['LossRatio'], 
                      color=segment_colors, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}',
                    ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        # Add reference lines
        plt.axhline(y=0.4, color='green', linestyle='--', linewidth=1.5, 
                   label='Low-Risk Threshold (0.40)', alpha=0.7)
        plt.axhline(y=0.7, color='orange', linestyle='--', linewidth=1.5, 
                   label='High-Risk Threshold (0.70)', alpha=0.7)
        
        plt.title('Loss Ratio by Risk Segment', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Risk Segment', fontsize=12, fontweight='bold')
        plt.ylabel('Loss Ratio (Claims / Premium)', fontsize=12, fontweight='bold')
        plt.legend(loc='upper right', fontsize=10)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        output_path = f'{self.output_dir}/loss_ratio_by_segment.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved: {output_path}")
        plt.close()
    
    def plot_segment_size_distribution(self, segment_counts):
        """Create pie chart of segment sizes"""
        print("\nCreating segment size distribution plot...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Pie chart
        colors = {'Low-Risk': '#2ecc71', 'Medium-Risk': '#f39c12', 'High-Risk': '#e74c3c'}
        segment_colors = [colors.get(seg, '#95a5a6') for seg in segment_counts['Segment']]
        
        wedges, texts, autotexts = ax1.pie(
            segment_counts['Count'],
            labels=segment_counts['Segment'],
            autopct='%1.1f%%',
            colors=segment_colors,
            startangle=90,
            textprops={'fontsize': 11, 'fontweight': 'bold'},
            explode=[0.05, 0, 0.05]
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)
            autotext.set_fontweight('bold')
        
        ax1.set_title('Segment Size Distribution', fontsize=14, fontweight='bold', pad=20)
        
        # Bar chart
        bars = ax2.bar(segment_counts['Segment'], segment_counts['Count'], 
                      color=segment_colors, edgecolor='black', linewidth=1.5)
        
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}',
                    ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        ax2.set_title('Customer Count by Segment', fontsize=14, fontweight='bold', pad=20)
        ax2.set_xlabel('Risk Segment', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Number of Customers', fontsize=11, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        output_path = f'{self.output_dir}/segment_size_distribution.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved: {output_path}")
        plt.close()
    
    def plot_premium_heatmap(self, geo_risk):
        """Create heatmap of average premium by province and segment"""
        print("\nCreating premium heatmap...")
        
        if geo_risk is None or geo_risk.empty:
            print("  No geographic data available, skipping heatmap")
            return
        
        # Pivot data for heatmap
        heatmap_data = geo_risk.pivot(
            index='Province',
            columns='RiskSegment',
            values='AvgPremium'
        )
        
        # Sort by total average premium
        heatmap_data['Total'] = heatmap_data.mean(axis=1)
        heatmap_data = heatmap_data.sort_values('Total', ascending=False).drop('Total', axis=1)
        
        # Reorder columns
        column_order = ['Low-Risk', 'Medium-Risk', 'High-Risk']
        heatmap_data = heatmap_data[[col for col in column_order if col in heatmap_data.columns]]
        
        plt.figure(figsize=(10, 8))
        
        sns.heatmap(
            heatmap_data,
            annot=True,
            fmt='.0f',
            cmap='RdYlGn_r',
            cbar_kws={'label': 'Average Premium (R)'},
            linewidths=0.5,
            linecolor='gray'
        )
        
        plt.title('Average Premium by Province and Risk Segment', 
                 fontsize=14, fontweight='bold', pad=20)
        plt.xlabel('Risk Segment', fontsize=11, fontweight='bold')
        plt.ylabel('Province', fontsize=11, fontweight='bold')
        plt.xticks(rotation=0)
        plt.yticks(rotation=0)
        plt.tight_layout()
        
        output_path = f'{self.output_dir}/premium_heatmap_province_segment.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved: {output_path}")
        plt.close()
    
    def save_summary_tables(self, segment_counts, segment_metrics, claims_dist, 
                           premium_stats, geo_risk):
        """Save all summary tables to CSV files"""
        print("\nSaving summary tables...")
        
        segment_counts.to_csv(f'{self.output_dir}/segment_counts.csv', index=False)
        print(f"  ✓ Saved: segment_counts.csv")
        
        segment_metrics.to_csv(f'{self.output_dir}/segment_metrics.csv', index=False)
        print(f"  ✓ Saved: segment_metrics.csv")
        
        claims_dist.to_csv(f'{self.output_dir}/claims_distribution.csv', index=False)
        print(f"  ✓ Saved: claims_distribution.csv")
        
        premium_stats.to_csv(f'{self.output_dir}/premium_statistics.csv', index=False)
        print(f"  ✓ Saved: premium_statistics.csv")
        
        if geo_risk is not None:
            geo_risk.to_csv(f'{self.output_dir}/geographic_risk.csv', index=False)
            print(f"  ✓ Saved: geographic_risk.csv")
    
    def generate_report(self, data_path):
        """Generate complete segment analysis report"""
        print("="*80)
        print("ACIS INSURANCE SEGMENT ANALYSIS REPORT")
        print("="*80)
        
        # Load data
        df = self.load_data(data_path)
        
        # Calculate metrics
        print("\n" + "="*80)
        print("CALCULATING SEGMENT METRICS")
        print("="*80)
        
        segment_counts = self.calculate_segment_counts(df)
        segment_metrics = self.calculate_loss_ratio_by_segment(df)
        claims_dist = self.calculate_claims_distribution(df)
        premium_stats = self.calculate_average_premium(df)
        geo_risk = self.compare_geographic_risk(df)
        
        # Generate visualizations
        print("\n" + "="*80)
        print("GENERATING VISUALIZATIONS")
        print("="*80)
        
        self.plot_loss_ratio_by_segment(segment_metrics)
        self.plot_segment_size_distribution(segment_counts)
        self.plot_premium_heatmap(geo_risk)
        
        # Save summary tables
        print("\n" + "="*80)
        print("SAVING SUMMARY TABLES")
        print("="*80)
        
        self.save_summary_tables(
            segment_counts, segment_metrics, claims_dist, 
            premium_stats, geo_risk
        )
        
        print("\n" + "="*80)
        print("SEGMENT ANALYSIS COMPLETE")
        print("="*80)
        print(f"\n✓ All outputs saved to: {self.output_dir}/")
        print("\nGenerated Files:")
        print("  Visualizations:")
        print("    - loss_ratio_by_segment.png")
        print("    - segment_size_distribution.png")
        print("    - premium_heatmap_province_segment.png")
        print("  Summary Tables:")
        print("    - segment_counts.csv")
        print("    - segment_metrics.csv")
        print("    - claims_distribution.csv")
        print("    - premium_statistics.csv")
        print("    - geographic_risk.csv")
        
        return {
            'segment_counts': segment_counts,
            'segment_metrics': segment_metrics,
            'claims_dist': claims_dist,
            'premium_stats': premium_stats,
            'geo_risk': geo_risk
        }


def main():
    """Main execution function"""
    # Configuration
    DATA_PATH = 'C:/Users/yoga/code/10_Academy/week_3/data/processed/train.parquet'
    OUTPUT_DIR = '../outputs/segments'
    
    # Check if processed data exists
    if not os.path.exists(DATA_PATH):
        print(f"ERROR: Processed data not found at {DATA_PATH}")
        print("Please run preprocess.py first to generate processed datasets.")
        return
    
    # Initialize reporter
    reporter = SegmentReporter(output_dir=OUTPUT_DIR)
    
    # Generate report
    results = reporter.generate_report(DATA_PATH)
    
    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("1. Review visualizations in outputs/segments/")
    print("2. Analyze summary tables for business insights")
    print("3. Present findings to leadership")
    print("4. Proceed to Task 3 for statistical hypothesis testing")
    print("="*80)


if __name__ == "__main__":
    main()
