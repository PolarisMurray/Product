from fastapi import APIRouter, HTTPException

from models.schemas import (
    PersonalAnalyzeRequest,
    PersonalAnalyzeResponse,
)

from services.genetics_engine import (
    interpret_snp,
    generate_peer_comparisons,
    generate_genetic_bio_card,
)

router = APIRouter(prefix="/analyze", tags=["personal"])


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

