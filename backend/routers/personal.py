from fastapi import APIRouter, HTTPException

from models.schemas import (
    PersonalAnalyzeRequest,
    PersonalAnalyzeResponse,
    SNPInput,
    PersonalInsightCard,
    PeerComparison,
    GeneticBioCard,
)

router = APIRouter(prefix="/analyze", tags=["personal"])


def interpret_snp(snp: SNPInput) -> PersonalInsightCard:
    """
    Simple rule-based SNP interpretation.
    
    This is a stub implementation. In production, this logic should be moved
    to a dedicated service module (e.g., services/genetics_engine.py) with
    a comprehensive rule database.
    """
    rsid = snp.rsid.lower()
    genotype = snp.genotype.upper()
    
    # Caffeine metabolism - rs762551 (CYP1A2)
    if rsid == "rs762551" or rsid == "rs123":
        if "A" in genotype:
            return PersonalInsightCard(
                domain="Caffeine Metabolism",
                summary="You have a variant associated with slower caffeine metabolism. This means caffeine may stay in your system longer, potentially affecting sleep quality if consumed later in the day.",
                score=0.65,
                percentile=0.35,  # Slower metabolism = lower percentile
                recommendations=[
                    "Consider limiting caffeine intake after 2 PM",
                    "Monitor how caffeine affects your sleep patterns",
                    "You may be more sensitive to caffeine's effects"
                ]
            )
        else:
            return PersonalInsightCard(
                domain="Caffeine Metabolism",
                summary="You have a variant associated with faster caffeine metabolism. You may process caffeine more quickly than average.",
                score=0.85,
                percentile=0.75,
                recommendations=[
                    "You may tolerate caffeine better than average",
                    "Still monitor your individual response to caffeine"
                ]
            )
    
    # Lactose tolerance - rs4988235 (LCT gene)
    elif rsid == "rs4988235":
        if "T" in genotype or genotype == "TT":
            return PersonalInsightCard(
                domain="Lactose Tolerance",
                summary="You carry a variant associated with lactose tolerance into adulthood. You likely digest lactose well.",
                score=0.90,
                percentile=0.80,
                recommendations=[
                    "You can likely consume dairy products without issues",
                    "Maintain a balanced diet including dairy if desired"
                ]
            )
        else:
            return PersonalInsightCard(
                domain="Lactose Tolerance",
                summary="You may have reduced lactose tolerance. Consider monitoring your response to dairy products.",
                score=0.40,
                percentile=0.30,
                recommendations=[
                    "Monitor your response to dairy products",
                    "Consider lactose-free alternatives if you experience discomfort",
                    "Fermented dairy (yogurt, kefir) may be better tolerated"
                ]
            )
    
    # Generic example trait
    else:
        return PersonalInsightCard(
            domain="Example Trait",
            summary=f"SNP {snp.rsid} with genotype {snp.genotype} detected. This is a placeholder interpretation for demonstration purposes.",
            score=0.50,
            percentile=0.50,
            recommendations=[
                "This is a stub recommendation",
                "Full interpretation will be available in production"
            ]
        )


def generate_peer_comparisons(cards: list[PersonalInsightCard]) -> list[PeerComparison]:
    """
    Generate peer comparison metrics based on insight cards.
    
    This is a stub implementation. In production, this should use
    population databases and statistical models.
    """
    comparisons = []
    
    # Find caffeine metabolism card if present
    caffeine_card = next((c for c in cards if "Caffeine" in c.domain), None)
    if caffeine_card:
        comparisons.append(PeerComparison(
            metric="caffeine_metabolism",
            value=caffeine_card.score,
            percentile=caffeine_card.percentile or 0.5,
            label="Caffeine Metabolism Speed"
        ))
    
    # Find lactose tolerance card if present
    lactose_card = next((c for c in cards if "Lactose" in c.domain), None)
    if lactose_card:
        comparisons.append(PeerComparison(
            metric="lactose_tolerance",
            value=lactose_card.score,
            percentile=lactose_card.percentile or 0.5,
            label="Lactose Tolerance"
        ))
    
    # Add a generic comparison if we have cards
    if cards:
        avg_score = sum(c.score for c in cards) / len(cards)
        comparisons.append(PeerComparison(
            metric="overall_genetic_profile",
            value=avg_score,
            percentile=0.55,
            label="Overall Genetic Profile"
        ))
    
    # Ensure we always return at least one comparison
    if not comparisons:
        comparisons.append(PeerComparison(
            metric="genetic_analysis",
            value=0.5,
            percentile=0.5,
            label="Genetic Analysis Complete"
        ))
    
    return comparisons


def generate_genetic_bio_card(cards: list[PersonalInsightCard], request: PersonalAnalyzeRequest) -> GeneticBioCard:
    """
    Generate a shareable genetic bio card.
    
    This is a stub implementation. In production, this should use
    AI-generated content based on the analysis results.
    """
    # Determine badges based on cards
    badges = []
    if any("Caffeine" in c.domain for c in cards):
        badges.append("Caffeine Analyzed")
    if any("Lactose" in c.domain for c in cards):
        badges.append("Lactose Analyzed")
    if len(cards) > 0:
        badges.append(f"{len(cards)} Traits Analyzed")
    
    # Generate highlights from card summaries
    highlights = []
    for card in cards[:3]:  # Top 3 cards
        highlights.append(f"{card.domain}: {card.summary[:80]}...")
    
    # Add lifestyle highlights if provided
    if request.lifestyle:
        lifestyle_parts = []
        if request.lifestyle.caffeine_intake:
            lifestyle_parts.append(f"Caffeine: {request.lifestyle.caffeine_intake}")
        if request.lifestyle.exercise_frequency:
            lifestyle_parts.append(f"Exercise: {request.lifestyle.exercise_frequency}")
        if lifestyle_parts:
            highlights.append(f"Lifestyle: {', '.join(lifestyle_parts)}")
    
    return GeneticBioCard(
        title="Personal Genetic Profile",
        subtitle=f"Analysis of {len(request.snps)} genetic variant(s)",
        badges=badges if badges else ["Genetic Analysis"],
        highlights=highlights if highlights else ["Genetic analysis completed successfully"]
    )


@router.post("/personal", response_model=PersonalAnalyzeResponse)
async def analyze_personal(request: PersonalAnalyzeRequest):
    """
    Analyze personal genomics data (SNPs + lifestyle).
    
    This endpoint accepts:
    - SNPs: List of SNP inputs with rsid and genotype
    - Lifestyle: Optional lifestyle factors (caffeine, exercise, sleep, diet)
    
    Returns personalized insights, peer comparisons, and a genetic bio card.
    """
    # Validate that we have at least one SNP
    if not request.snps:
        raise HTTPException(status_code=400, detail="At least one SNP must be provided")
    
    # Interpret each SNP and create insight cards
    cards = []
    for snp in request.snps:
        card = interpret_snp(snp)
        cards.append(card)
    
    # Generate peer comparisons
    peer_comparison = generate_peer_comparisons(cards)
    
    # Generate genetic bio card
    genetic_card = generate_genetic_bio_card(cards, request)
    
    return PersonalAnalyzeResponse(
        cards=cards,
        peer_comparison=peer_comparison,
        genetic_card=genetic_card
    )

