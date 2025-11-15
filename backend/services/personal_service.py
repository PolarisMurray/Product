import numpy as np
from scipy import stats
from typing import Optional


def compute_peer_percentile(score: float, distribution_type: str = "normal") -> float:
    """
    Map internal score (0-1) to percentile (0-1) using statistical distributions.
    
    This implementation uses parametric distributions to model population data.
    In production, this would use actual reference cohort data from population
    genomics databases (e.g., 1000 Genomes, gnomAD, UK Biobank).
    
    Args:
        score: Internal score value between 0 and 1
        distribution_type: Type of distribution to use ("normal", "beta", "uniform")
    
    Returns:
        Percentile value between 0 and 1 (0 = bottom percentile, 1 = top percentile)
    """
    # Validate input range
    if score < 0:
        score = 0.0
    elif score > 1:
        score = 1.0
    
    # Use different distributions based on type
    if distribution_type == "normal":
        # Normal distribution centered at 0.5 with std=0.2
        # This creates a bell curve where most people are near average
        mean = 0.5
        std = 0.2
        # Convert score to percentile using CDF
        percentile = stats.norm.cdf(score, loc=mean, scale=std)
    
    elif distribution_type == "beta":
        # Beta distribution (alpha=2, beta=2) creates a symmetric bell curve
        # This is good for traits that cluster around the middle
        alpha, beta = 2.0, 2.0
        percentile = stats.beta.cdf(score, alpha, beta)
    
    elif distribution_type == "uniform":
        # Uniform distribution (all scores equally likely)
        percentile = score
    
    else:
        # Default to normal
        mean = 0.5
        std = 0.2
        percentile = stats.norm.cdf(score, loc=mean, scale=std)
    
    # Ensure percentile is in valid range [0, 1]
    percentile = max(0.0, min(1.0, percentile))
    
    return percentile


def compute_trait_specific_percentile(score: float, trait: str) -> float:
    """
    Compute percentile for a specific trait using trait-specific distributions.
    
    Different traits may have different population distributions:
    - Some traits are normally distributed (e.g., height)
    - Others may be skewed (e.g., rare disease risk)
    - Some may be bimodal (e.g., lactose tolerance)
    
    Args:
        score: Internal score value between 0 and 1
        trait: Trait name (e.g., "caffeine_metabolism", "lactose_tolerance")
    
    Returns:
        Percentile value between 0 and 1
    """
    # Trait-specific distribution parameters
    trait_distributions = {
        "caffeine_metabolism": {
            "type": "normal",
            "mean": 0.5,
            "std": 0.25,  # Wider distribution
        },
        "lactose_tolerance": {
            "type": "beta",
            "alpha": 1.5,
            "beta": 3.0,  # Skewed toward lower tolerance
        },
        "cardiovascular_health": {
            "type": "normal",
            "mean": 0.6,
            "std": 0.15,  # Slightly shifted toward better health
        },
        "drug_metabolism": {
            "type": "normal",
            "mean": 0.5,
            "std": 0.2,
        },
        "exercise_response": {
            "type": "normal",
            "mean": 0.55,
            "std": 0.18,
        },
    }
    
    # Get distribution for this trait, or use default
    dist_params = trait_distributions.get(trait.lower(), {
        "type": "normal",
        "mean": 0.5,
        "std": 0.2,
    })
    
    # Compute percentile based on distribution type
    if dist_params["type"] == "normal":
        percentile = stats.norm.cdf(
            score, 
            loc=dist_params["mean"], 
            scale=dist_params["std"]
        )
    elif dist_params["type"] == "beta":
        percentile = stats.beta.cdf(
            score,
            dist_params.get("alpha", 2.0),
            dist_params.get("beta", 2.0)
        )
    else:
        percentile = compute_peer_percentile(score)
    
    return max(0.0, min(1.0, percentile))

