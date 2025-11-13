"""
Agent 3: Investigator Agent - The Fact-Checker
Searches fact-check databases, performs reverse image search, verifies sources
"""

import asyncio
import logging
from typing import Dict, List, Optional
import aiohttp
from datetime import datetime

logger = logging.getLogger(__name__)


class InvestigatorAgent:
    """
    Investigator Agent collects evidence from fact-checking databases,
    performs reverse image searches, and verifies source credibility
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.google_factcheck_api_key = config.get('google_factcheck_api_key')
        self.tineye_api_key = config.get('tineye_api_key')
        
        # Known fact-checking sources
        self.factcheck_sources = [
            'snopes.com',
            'politifact.com',
            'factcheck.org',
            'afp.com/factcheck'
        ]
        
        # Known reliable news sources
        self.credible_domains = [
            'reuters.com', 'apnews.com', 'bbc.com', 'npr.org',
            'nytimes.com', 'washingtonpost.com', 'theguardian.com'
        ]
        
        # Known fake news sites
        self.fake_domains = [
            'naturalnews.com', 'infowars.com', 'beforeitsnews.com'
        ]
        
        logger.info("✅ Investigator Agent initialized")
    
    async def investigate(self, analysis_report: Dict) -> Dict:
        """
        Comprehensive fact-checking and evidence collection
        
        Args:
            analysis_report: Report from Analyst Agent
            
        Returns:
            Evidence report with debunks, sources, credibility scores
        """
        try:
            content_id = analysis_report.get('content_id')
            logger.info(f"🔎 Investigating content: {content_id}")
            
            # Step 3.1: Search fact-check databases
            factcheck_results = await self._search_factcheck_databases(analysis_report)
            
            # Step 3.2: Reverse image search
            image_results = await self._reverse_image_search(analysis_report)
            
            # Step 3.3: Source credibility check
            credibility_score = await self._check_source_credibility(analysis_report)
            
            # Step 3.4: Compile evidence report
            evidence_report = self._compile_evidence_report(
                analysis_report,
                factcheck_results,
                image_results,
                credibility_score
            )
            
            logger.info(
                f"✅ Investigation complete: {content_id} - "
                f"Verdict: {evidence_report['verdict']}"
            )
            
            return evidence_report
            
        except Exception as e:
            logger.error(f"Error investigating content: {e}", exc_info=True)
            return self._error_report(analysis_report)
    
    async def _search_factcheck_databases(self, report: Dict) -> List[Dict]:
        """
        Query external fact-checking APIs and databases
        """
        results = []
        
        # Extract key claims from text analysis
        text_analysis = report.get('text_analysis', {})
        claims = text_analysis.get('key_claims', [])
        text = report.get('source_data', {}).get('text', '')
        
        # Google Fact Check API
        if self.google_factcheck_api_key:
            google_results = await self._query_google_factcheck(text)
            results.extend(google_results)
        
        # Additional fact-check sources (web scraping)
        # In production: implement Snopes, PolitiFact scrapers
        
        return results
    
    async def _query_google_factcheck(self, query: str) -> List[Dict]:
        """Query Google Fact Check Tools API"""
        try:
            url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
            params = {
                'query': query[:100],  # Limit query length
                'key': self.google_factcheck_api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        claims = data.get('claims', [])
                        
                        results = []
                        for claim in claims[:3]:  # Top 3 results
                            review = claim.get('claimReview', [{}])[0]
                            results.append({
                                'source': review.get('publisher', {}).get('name', 'Unknown'),
                                'url': review.get('url', ''),
                                'title': review.get('title', ''),
                                'rating': review.get('textualRating', ''),
                                'date': claim.get('claimDate', '')
                            })
                        
                        return results
        except Exception as e:
            logger.error(f"Google Fact Check API error: {e}")
        
        return []
    
    async def _reverse_image_search(self, report: Dict) -> Dict:
        """
        Perform reverse image search to find original source
        """
        images = report.get('source_data', {}).get('images', [])
        
        if not images:
            return {'found_original': False}
        
        # Placeholder for TinEye/Google Images API integration
        # In production: implement actual reverse search
        
        return {
            'found_original': False,
            'original_date': None,
            'original_context': None,
            'misuse_detected': False
        }
    
    async def _check_source_credibility(self, report: Dict) -> Dict:
        """
        Check the credibility of the content source
        """
        metadata = report.get('source_data', {}).get('metadata', {})
        url = metadata.get('url', '')
        author = metadata.get('author', {})
        
        # Domain reputation check
        domain_score = self._check_domain_reputation(url)
        
        # Author credibility check
        author_score = self._check_author_credibility(author)
        
        # Overall credibility score (0-100)
        credibility_score = (domain_score + author_score) / 2
        
        return {
            'overall_score': credibility_score,
            'domain_score': domain_score,
            'author_score': author_score,
            'is_verified_source': domain_score > 80,
            'is_known_fake_source': domain_score < 20
        }
    
    def _check_domain_reputation(self, url: str) -> int:
        """
        Check if domain is credible, neutral, or known for fake news
        Returns: Score 0-100
        """
        if not url:
            return 50  # Neutral if no URL
        
        url_lower = url.lower()
        
        # Check against credible sources
        if any(domain in url_lower for domain in self.credible_domains):
            return 95
        
        # Check against known fake news sites
        if any(domain in url_lower for domain in self.fake_domains):
            return 10
        
        # Default: neutral/unknown
        return 50
    
    def _check_author_credibility(self, author: Dict) -> int:
        """
        Check author's credibility based on profile
        Returns: Score 0-100
        """
        if not author:
            return 50
        
        score = 50  # Base score
        
        # Verified account bonus
        if author.get('verified', False):
            score += 20
        
        # Account age (older = more credible)
        account_age_days = author.get('account_age_days', 0)
        if account_age_days > 365:
            score += 15
        elif account_age_days < 30:
            score -= 20
        
        # Follower count (logarithmic scale)
        followers = author.get('followers', 0)
        if followers > 10000:
            score += 10
        elif followers < 100:
            score -= 10
        
        # Past misinformation history
        if author.get('misinformation_history', False):
            score -= 30
        
        return max(0, min(100, score))
    
    def _compile_evidence_report(
        self,
        analysis_report: Dict,
        factcheck_results: List[Dict],
        image_results: Dict,
        credibility: Dict
    ) -> Dict:
        """
        Compile all evidence into structured report
        """
        # Determine verdict based on evidence
        fake_prob = analysis_report.get('fake_probability', 0.5)
        has_debunks = len(factcheck_results) > 0
        low_credibility = credibility['overall_score'] < 40
        
        # Confidence in verdict
        confidence = 0.7  # Base confidence
        if has_debunks:
            confidence += 0.2
        if low_credibility:
            confidence += 0.1
        
        verdict = 'FALSE' if fake_prob > 0.7 else 'UNVERIFIED' if fake_prob > 0.5 else 'TRUE'
        
        return {
            'content_id': analysis_report.get('content_id'),
            'verdict': verdict,
            'confidence': min(confidence, 1.0),
            'fake_probability': fake_prob,
            'debunks': factcheck_results,
            'image_source': image_results,
            'source_credibility': credibility,
            'evidence_strength': self._calculate_evidence_strength(
                factcheck_results, credibility
            ),
            'investigation_timestamp': datetime.utcnow().isoformat(),
            'analysis_report': analysis_report
        }
    
    def _calculate_evidence_strength(
        self,
        debunks: List[Dict],
        credibility: Dict
    ) -> float:
        """
        Calculate overall strength of evidence (0-1)
        """
        strength = 0.5  # Base
        
        # More debunks = stronger evidence
        if len(debunks) >= 3:
            strength += 0.3
        elif len(debunks) >= 1:
            strength += 0.2
        
        # Low source credibility = stronger evidence of fake
        if credibility['overall_score'] < 30:
            strength += 0.2
        
        return min(strength, 1.0)
    
    def _error_report(self, report: Dict) -> Dict:
        """Return error report if investigation fails"""
        return {
            'content_id': report.get('content_id'),
            'verdict': 'UNVERIFIED',
            'confidence': 0.3,
            'error': True,
            'analysis_report': report
        }
