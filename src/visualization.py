"""
Visualization Utilities for AlphaCare Insurance Solutions
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List, Tuple


def set_plot_style(style: str = 'whitegrid', context: str = 'notebook'):
    """
    Set default plotting style.
    
    Parameters:
    -----------
    style : str, default 'whitegrid'
        Seaborn style
    context : str, default 'notebook'
        Seaborn context
    """
    sns.set_style(style)
    sns.set_context(context)
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 10


def plot_loss_ratio_by_group(data: pd.DataFrame,
                             group_col: str,
                             loss_ratio_col: str = 'LossRatio',
                             title: str = 'Loss Ratio by Group',
                             save_path: Optional[str] = None,
                             figsize: Tuple[int, int] = (12, 6)) -> None:
    """
    Plot loss ratio by group with color coding.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Grouped data with loss ratios
    group_col : str
        Column name for groups
    loss_ratio_col : str, default 'LossRatio'
        Column name for loss ratios
    title : str
        Plot title
    save_path : str, optional
        Path to save the plot
    figsize : tuple, default (12, 6)
        Figure size
    """
    plt.figure(figsize=figsize)
    
    colors = ['green' if x < 100 else 'red' for x in data[loss_ratio_col]]
    
    plt.barh(data[group_col], data[loss_ratio_col], color=colors, alpha=0.7)
    plt.axvline(x=100, color='black', linestyle='--', linewidth=2, label='Break-even (100%)')
    plt.xlabel('Loss Ratio (%)', fontsize=12)
    plt.ylabel(group_col, fontsize=12)
    plt.title(f'{title}\n(Green = Profitable, Red = Unprofitable)', fontsize=14, fontweight='bold')
    plt.legend()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    plt.show()


def plot_missing_values(missing_data: pd.DataFrame,
                       top_n: int = 20,
                       save_path: Optional[str] = None,
                       figsize: Tuple[int, int] = (12, 8)) -> None:
    """
    Plot missing values analysis.
    
    Parameters:
    -----------
    missing_data : pd.DataFrame
        Missing values summary
    top_n : int, default 20
        Number of top columns to show
    save_path : str, optional
        Path to save the plot
    figsize : tuple, default (12, 8)
        Figure size
    """
    if len(missing_data) == 0:
        print("No missing values to plot")
        return
    
    top_missing = missing_data.head(top_n)
    
    plt.figure(figsize=figsize)
    plt.barh(top_missing['Column'], top_missing['Missing_Percentage'], color='coral')
    plt.xlabel('Missing Percentage (%)', fontsize=12)
    plt.ylabel('Column', fontsize=12)
    plt.title(f'Top {top_n} Columns with Missing Values', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    plt.show()


def plot_time_series(data: pd.DataFrame,
                    date_col: str,
                    value_cols: List[str],
                    labels: Optional[List[str]] = None,
                    title: str = 'Time Series Plot',
                    save_path: Optional[str] = None,
                    figsize: Tuple[int, int] = (14, 6)) -> None:
    """
    Plot time series data.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Time series data
    date_col : str
        Date column name
    value_cols : list
        List of value columns to plot
    labels : list, optional
        Labels for each value column
    title : str
        Plot title
    save_path : str, optional
        Path to save the plot
    figsize : tuple, default (14, 6)
        Figure size
    """
    if labels is None:
        labels = value_cols
    
    plt.figure(figsize=figsize)
    
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    markers = ['o', 's', '^', 'D', 'v']
    
    for i, (col, label) in enumerate(zip(value_cols, labels)):
        plt.plot(data[date_col], data[col], 
                marker=markers[i % len(markers)], 
                linewidth=2, 
                color=colors[i % len(colors)], 
                label=label)
    
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Amount', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    plt.show()


def plot_correlation_matrix(df: pd.DataFrame,
                           columns: Optional[List[str]] = None,
                           title: str = 'Correlation Matrix',
                           save_path: Optional[str] = None,
                           figsize: Tuple[int, int] = (16, 14)) -> None:
    """
    Plot correlation matrix heatmap.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    columns : list, optional
        Columns to include in correlation
    title : str
        Plot title
    save_path : str, optional
        Path to save the plot
    figsize : tuple, default (16, 14)
        Figure size
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    correlation_matrix = df[columns].corr()
    
    plt.figure(figsize=figsize)
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    plt.show()


def plot_boxplot_by_group(df: pd.DataFrame,
                         group_col: str,
                         value_col: str,
                         top_n: Optional[int] = None,
                         title: str = 'Boxplot by Group',
                         save_path: Optional[str] = None,
                         figsize: Tuple[int, int] = (14, 8)) -> None:
    """
    Plot boxplot by group.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    group_col : str
        Column to group by
    value_col : str
        Value column to plot
    top_n : int, optional
        Number of top groups to show
    title : str
        Plot title
    save_path : str, optional
        Path to save the plot
    figsize : tuple, default (14, 8)
        Figure size
    """
    if top_n:
        top_groups = df[group_col].value_counts().head(top_n).index
        df_plot = df[df[group_col].isin(top_groups)].copy()
    else:
        df_plot = df.copy()
    
    plt.figure(figsize=figsize)
    sns.boxplot(data=df_plot, y=group_col, x=value_col, palette='Set2')
    plt.xlabel(value_col, fontsize=12)
    plt.ylabel(group_col, fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    plt.show()


def plot_distribution(df: pd.DataFrame,
                     columns: List[str],
                     bins: int = 50,
                     title: str = 'Distribution Plot',
                     save_path: Optional[str] = None,
                     figsize: Tuple[int, int] = (16, 6)) -> None:
    """
    Plot distribution histograms.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    columns : list
        Columns to plot
    bins : int, default 50
        Number of bins
    title : str
        Plot title
    save_path : str, optional
        Path to save the plot
    figsize : tuple, default (16, 6)
        Figure size
    """
    n_cols = len(columns)
    fig, axes = plt.subplots(1, n_cols, figsize=figsize)
    
    if n_cols == 1:
        axes = [axes]
    
    colors = ['skyblue', 'coral', 'lightgreen', 'gold']
    
    for i, col in enumerate(columns):
        axes[i].hist(df[col], bins=bins, color=colors[i % len(colors)], 
                    edgecolor='black', alpha=0.7)
        axes[i].set_xlabel(col, fontsize=12)
        axes[i].set_ylabel('Frequency', fontsize=12)
        axes[i].set_title(f'Distribution of {col}', fontsize=12, fontweight='bold')
        axes[i].axvline(df[col].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
        axes[i].axvline(df[col].median(), color='green', linestyle='--', linewidth=2, label='Median')
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)
    
    plt.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    plt.show()


def plot_scatter(df: pd.DataFrame,
                x_col: str,
                y_col: str,
                sample_size: Optional[int] = None,
                title: str = 'Scatter Plot',
                save_path: Optional[str] = None,
                figsize: Tuple[int, int] = (12, 8)) -> None:
    """
    Plot scatter plot with optional sampling.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    x_col : str
        X-axis column
    y_col : str
        Y-axis column
    sample_size : int, optional
        Number of samples to plot
    title : str
        Plot title
    save_path : str, optional
        Path to save the plot
    figsize : tuple, default (12, 8)
        Figure size
    """
    if sample_size and sample_size < len(df):
        df_plot = df.sample(n=sample_size, random_state=42)
    else:
        df_plot = df
    
    plt.figure(figsize=figsize)
    plt.scatter(df_plot[x_col], df_plot[y_col], alpha=0.5, s=20, 
               c='steelblue', edgecolors='none')
    
    # Add diagonal line (break-even for premium vs claims)
    if 'Premium' in x_col and 'Claims' in y_col:
        max_val = max(df_plot[x_col].max(), df_plot[y_col].max())
        plt.plot([0, max_val], [0, max_val], 'r--', linewidth=2, label='Break-even line')
        plt.legend()
    
    plt.xlabel(x_col, fontsize=12)
    plt.ylabel(y_col, fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    plt.show()
