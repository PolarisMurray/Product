"""
Genetics interpretation engine for SNP analysis.

This module provides functions to interpret SNPs and generate insights.
"""
from typing import List, Dict, Any, Optional
from models.schemas import SNPInput, PersonalInsightCard, GeneticBioCard, PeerComparison
from services.personal_service import compute_peer_percentile, compute_trait_specific_percentile


# SNP rule database
# In production, this would be loaded from a database or external API
SNP_RULES = {
    "rs762551": {
        "domain": "Caffeine Metabolism",
        "gene": "CYP1A2",
        "description": "CYP1A2 enzyme activity affects caffeine metabolism speed",
        "genotypes": {
            "AA": {
                "interpretation": "Fast caffeine metabolizer",
                "score": 0.8,
                "recommendations": [
                    "You metabolize caffeine quickly",
                    "May tolerate higher caffeine intake",
                    "Caffeine effects may be shorter-lived"
                ]
            },
            "AC": {
                "interpretation": "Intermediate caffeine metabolizer",
                "score": 0.5,
                "recommendations": [
                    "Moderate caffeine metabolism",
                    "Standard caffeine recommendations apply",
                    "Monitor your response to caffeine"
                ]
            },
            "CC": {
                "interpretation": "Slow caffeine metabolizer",
                "score": 0.2,
                "recommendations": [
                    "You metabolize caffeine slowly",
                    "Consider limiting caffeine intake, especially in afternoon",
                    "May experience longer-lasting effects from caffeine",
                    "Higher risk of sleep disruption from caffeine"
                ]
            }
        }
    },
    "rs4988235": {
        "domain": "Lactose Tolerance",
        "gene": "LCT",
        "description": "Lactase persistence affects ability to digest lactose",
        "genotypes": {
            "CC": {
                "interpretation": "Lactose tolerant",
                "score": 0.9,
                "recommendations": [
                    "You can digest lactose well",
                    "No need to avoid dairy products",
                    "Lactose intolerance is unlikely"
                ]
            },
            "CT": {
                "interpretation": "Partial lactose tolerance",
                "score": 0.6,
                "recommendations": [
                    "Moderate lactose tolerance",
                    "May tolerate small amounts of dairy",
                    "Monitor symptoms after dairy consumption"
                ]
            },
            "TT": {
                "interpretation": "Lactose intolerant",
                "score": 0.1,
                "recommendations": [
                    "Likely lactose intolerant",
                    "Consider limiting dairy intake",
                    "Try lactose-free alternatives",
                    "Monitor for digestive symptoms"
                ]
            }
        }
    },
    "rs7412": {
        "domain": "Cardiovascular Health",
        "gene": "APOE",
        "description": "APOE ε2 variant associated with cardiovascular health",
        "genotypes": {
            "CC": {
                "interpretation": "APOE ε2/ε2 - Lower cardiovascular risk",
                "score": 0.85,
                "recommendations": [
                    "Favorable APOE profile for cardiovascular health",
                    "Continue heart-healthy lifestyle",
                    "Regular cardiovascular monitoring recommended"
                ]
            },
            "CT": {
                "interpretation": "APOE ε2/ε3 - Moderate cardiovascular risk",
                "score": 0.6,
                "recommendations": [
                    "Standard cardiovascular risk profile",
                    "Maintain heart-healthy diet and exercise",
                    "Regular health checkups recommended"
                ]
            },
            "TT": {
                "interpretation": "APOE ε3/ε3 - Standard cardiovascular risk",
                "score": 0.5,
                "recommendations": [
                    "Standard cardiovascular risk profile",
                    "Follow general heart health guidelines",
                    "Regular monitoring recommended"
                ]
            }
        }
    },
    "rs1800566": {
        "domain": "Drug Metabolism",
        "gene": "CYP2D6",
        "description": "CYP2D6 enzyme affects metabolism of many medications",
        "genotypes": {
            "GG": {
                "interpretation": "Normal CYP2D6 metabolizer",
                "score": 0.7,
                "recommendations": [
                    "Normal drug metabolism",
                    "Standard medication dosages typically appropriate",
                    "Discuss with healthcare provider for medication adjustments"
                ]
            },
            "GA": {
                "interpretation": "Intermediate CYP2D6 metabolizer",
                "score": 0.5,
                "recommendations": [
                    "Moderate drug metabolism",
                    "May require adjusted dosages for some medications",
                    "Consult healthcare provider about pharmacogenetics"
                ]
            },
            "AA": {
                "interpretation": "Poor CYP2D6 metabolizer",
                "score": 0.3,
                "recommendations": [
                    "Reduced drug metabolism",
                    "May require lower dosages for some medications",
                    "Important to discuss with healthcare provider",
                    "Consider pharmacogenetic testing for medications"
                ]
            }
        }
    },
    "rs1042713": {
        "domain": "Exercise Response",
        "gene": "ADRB2",
        "description": "Beta-2 adrenergic receptor affects exercise performance",
        "genotypes": {
            "GG": {
                "interpretation": "Enhanced exercise response",
                "score": 0.75,
                "recommendations": [
                    "Favorable genetics for endurance exercise",
                    "May respond well to aerobic training",
                    "Consider endurance-focused training programs"
                ]
            },
            "AG": {
                "interpretation": "Moderate exercise response",
                "score": 0.5,
                "recommendations": [
                    "Standard exercise response",
                    "Balanced training approach recommended",
                    "Both strength and cardio training beneficial"
                ]
            },
            "AA": {
                "interpretation": "Standard exercise response",
                "score": 0.45,
                "recommendations": [
                    "Standard exercise genetics",
                    "Consistent training is key",
                    "Focus on progressive overload"
                ]
            }
        }
    }
}


def interpret_snp(snp: SNPInput) -> PersonalInsightCard:
    """
    Interpret a single SNP and generate an insight card.
    
    Args:
        snp: SNPInput with rsid and genotype
    
    Returns:
        PersonalInsightCard with interpretation
    """
    rsid = snp.rsid.upper()
    genotype = snp.genotype.upper()
    
    # Check if we have rules for this SNP
    if rsid not in SNP_RULES:
        # Generic card for unknown SNPs
        return PersonalInsightCard(
            domain="Genetic Variant",
            summary=f"SNP {rsid} with genotype {genotype} detected. This variant may have functional significance, but specific interpretation requires additional research.",
            score=0.5,
            percentile=None,
            recommendations=[
                "Consult with a genetic counselor or healthcare provider",
                "Review scientific literature for this variant",
                "Consider additional genetic testing if clinically relevant"
            ]
        )
    
    rule = SNP_RULES[rsid]
    
    # Get genotype-specific interpretation
    if genotype not in rule["genotypes"]:
        # If exact genotype not found, try to find closest match or use default
        # For now, use the first available genotype as fallback
        available_genotypes = list(rule["genotypes"].keys())
        genotype_data = rule["genotypes"][available_genotypes[0]]
        interpretation_note = f"Note: Genotype {genotype} interpretation may vary. Showing reference interpretation."
    else:
        genotype_data = rule["genotypes"][genotype]
        interpretation_note = ""
    
    # Calculate percentile using trait-specific distribution
    score = genotype_data["score"]
    # Map domain to trait name for percentile calculation
    trait_name = rule["domain"].lower().replace(" ", "_")
    percentile = compute_trait_specific_percentile(score, trait_name)
    
    # Build summary
    summary_parts = [
        f"{rule['domain']}: {genotype_data['interpretation']}",
        f"Gene: {rule['gene']}",
        rule['description']
    ]
    if interpretation_note:
        summary_parts.append(interpretation_note)
    
    summary = ". ".join(summary_parts) + "."
    
    return PersonalInsightCard(
        domain=rule["domain"],
        summary=summary,
        score=score,
        percentile=percentile,
        recommendations=genotype_data["recommendations"]
    )


def generate_peer_comparisons(cards: List[PersonalInsightCard]) -> List[PeerComparison]:
    """
    Generate peer comparison metrics based on insight cards.
    
    Args:
        cards: List of PersonalInsightCard objects
    
    Returns:
        List of PeerComparison objects
    """
    if not cards:
        return []
    
    comparisons = []
    
    # Calculate average score
    avg_score = sum(card.score for card in cards) / len(cards) if cards else 0.5
    avg_percentile = compute_peer_percentile(avg_score)
    
    comparisons.append(PeerComparison(
        metric="Overall Genetic Score",
        value=round(avg_score, 2),
        percentile=round(avg_percentile, 2),
        label="Average across all analyzed traits"
    ))
    
    # Add domain-specific comparisons
    domain_scores = {}
    for card in cards:
        if card.domain not in domain_scores:
            domain_scores[card.domain] = []
        domain_scores[card.domain].append(card.score)
    
    for domain, scores in domain_scores.items():
        domain_avg = sum(scores) / len(scores)
        domain_percentile = compute_peer_percentile(domain_avg)
        comparisons.append(PeerComparison(
            metric=domain,
            value=round(domain_avg, 2),
            percentile=round(domain_percentile, 2),
            label=f"Average score in {domain}"
        ))
    
    return comparisons


def generate_genetic_bio_card(cards: List[PersonalInsightCard], 
                             lifestyle: Optional[Any] = None) -> GeneticBioCard:
    """
    Generate a genetic bio card summarizing the analysis.
    
    Args:
        cards: List of PersonalInsightCard objects
        lifestyle: Optional lifestyle input
    
    Returns:
        GeneticBioCard object
    """
    if not cards:
        return GeneticBioCard(
            title="Genetic Profile",
            subtitle="No genetic variants analyzed",
            badges=[],
            highlights=["Upload SNP data to generate your genetic profile"]
        )
    
    # Calculate overall metrics
    avg_score = sum(card.score for card in cards) / len(cards)
    num_domains = len(set(card.domain for card in cards))
    
    # Generate title and subtitle
    title = "Personal Genetic Profile"
    subtitle = f"Analysis of {len(cards)} genetic variant{'s' if len(cards) != 1 else ''} across {num_domains} domain{'s' if num_domains != 1 else ''}"
    
    # Generate badges (top domains)
    domain_counts = {}
    for card in cards:
        domain_counts[card.domain] = domain_counts.get(card.domain, 0) + 1
    
    badges = [f"{domain}" for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:5]]
    
    # Generate highlights
    highlights = []
    
    # Add top insights
    top_cards = sorted(cards, key=lambda x: abs(x.score - 0.5), reverse=True)[:3]
    for card in top_cards:
        if card.score > 0.7:
            highlights.append(f"Strong positive signal in {card.domain}")
        elif card.score < 0.3:
            highlights.append(f"Notable variant in {card.domain}")
    
    # Add lifestyle integration if available
    if lifestyle:
        if hasattr(lifestyle, 'exercise_frequency') and lifestyle.exercise_frequency:
            highlights.append(f"Exercise frequency: {lifestyle.exercise_frequency}")
        if hasattr(lifestyle, 'caffeine_intake') and lifestyle.caffeine_intake:
            highlights.append(f"Caffeine intake: {lifestyle.caffeine_intake}")
    
    # Add overall summary
    if avg_score > 0.6:
        highlights.insert(0, "Overall favorable genetic profile")
    elif avg_score < 0.4:
        highlights.insert(0, "Some genetic variants may require attention")
    else:
        highlights.insert(0, "Balanced genetic profile")
    
    return GeneticBioCard(
        title=title,
        subtitle=subtitle,
        badges=badges,
        highlights=highlights
    )

