import os
import asyncio
from typing import Dict, Any, Optional
import google.generativeai as genai

# Simple result class without Pydantic
class SimpleAnswerResult:
    def __init__(self, answer: str, confidence: float, reasoning: str = ""):
        self.answer = answer
        self.confidence = confidence
        self.reasoning = reasoning

from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class LLMService:
    """
    LLM service for generating accurate answers from document context
    Specialized for insurance policies and legal document analysis using Google Gemini
    """
    
    def __init__(self):
        # Configure Gemini API
        api_key = os.getenv("GEMINI_API_KEY")  # Using Gemini API key
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable must be set with your Gemini API key")
        
        genai.configure(api_key=api_key)
        self.model_name = os.getenv("MODEL_NAME", "gemini-1.5-flash")
        self.model = genai.GenerativeModel(self.model_name)
        self.max_tokens = 500
        self.temperature = 0.1  # Low temperature for factual answers
        
        # Specialized prompt template for insurance/legal documents
        self.prompt_template = """You are a domain expert in insurance policies and legal document analysis.

Given a document and a user question, extract an accurate, concise, and contextually matched answer directly from the document.

Instructions:
- Do not infer or assume facts not present in the document.
- Focus on clauses that best match the question intent.
- Answer in 1-2 sentences with clarity and precision.
- If no direct answer exists, respond: "The document does not provide a specific answer to this question."
- Always cite the specific section or clause where you found the information.
- Be precise with numbers, dates, and specific terms.

Context Document (Extracted):
{context}

Question:
{question}

Answer:"""

    async def generate_answer(self, question: str, context: str) -> SimpleAnswerResult:
        """
        Generate an answer for a question using the provided context
        
        Args:
            question: The question to answer
            context: Relevant document context
            
        Returns:
            SimpleAnswerResult with the generated answer and metadata
        """
        try:
            logger.info(f"Generating answer for question: {question[:50]}...")
            
            # Format the prompt
            formatted_prompt = self.prompt_template.format(
                context=context,
                question=question
            )
            
            # Generate answer using Gemini
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.model.generate_content(
                    formatted_prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=self.max_tokens,
                        temperature=self.temperature,
                        top_p=0.9,
                        top_k=40
                    )
                )
            )
            
            answer_text = response.text.strip()
            
            # Calculate confidence based on answer characteristics
            confidence = self._calculate_confidence(answer_text, context, question)
            
            # Extract source chunks (first 3 sentences of context for brevity)
            source_chunks = self._extract_source_chunks(context)
            
            # Generate reasoning
            reasoning = self._generate_reasoning(answer_text, question)
            
            result = SimpleAnswerResult(
                question=question,
                answer=answer_text,
                confidence=confidence,
                source_chunks=source_chunks,
                reasoning=reasoning
            )
            
            logger.info(f"Generated answer with confidence: {confidence:.2f}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            
            # Return a fallback answer
            return SimpleAnswerResult(
                question=question,
                answer="An error occurred while processing this question. Please try again.",
                confidence=0.0,
                source_chunks=[],
                reasoning=f"Error: {str(e)}"
            )
    
    def _calculate_confidence(self, answer: str, context: str, question: str) -> float:
        """
        Calculate confidence score for the answer
        
        Args:
            answer: Generated answer
            context: Source context
            question: Original question
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        try:
            confidence = 0.5  # Base confidence
            
            # Check if answer indicates uncertainty
            uncertainty_phrases = [
                "does not provide",
                "not specified",
                "unclear",
                "not mentioned",
                "cannot determine"
            ]
            
            if any(phrase in answer.lower() for phrase in uncertainty_phrases):
                confidence = 0.3
            else:
                # Higher confidence for specific answers
                if any(indicator in answer.lower() for indicator in ["section", "clause", "paragraph", "$", "%"]):
                    confidence += 0.3
                
                # Check answer length (too short might be less reliable)
                if 20 <= len(answer) <= 200:
                    confidence += 0.1
                
                # Check if question words appear in context
                question_words = question.lower().split()
                context_lower = context.lower()
                matching_words = sum(1 for word in question_words if word in context_lower)
                if matching_words > len(question_words) * 0.3:
                    confidence += 0.1
            
            return min(max(confidence, 0.0), 1.0)  # Clamp between 0 and 1
            
        except Exception:
            return 0.5  # Default confidence
    
    def _extract_source_chunks(self, context: str, max_chunks: int = 3) -> list:
        """
        Extract representative source chunks from context
        
        Args:
            context: Full context text
            max_chunks: Maximum number of chunks to return
            
        Returns:
            List of source text chunks
        """
        try:
            # Split context into sentences
            sentences = [s.strip() + '.' for s in context.split('.') if s.strip()]
            
            # Return first few sentences as source chunks
            return sentences[:max_chunks] if sentences else [context[:200] + "..."]
            
        except Exception:
            return [context[:200] + "..."]
    
    def _generate_reasoning(self, answer: str, question: str) -> str:
        """
        Generate simple reasoning for the answer
        
        Args:
            answer: Generated answer
            question: Original question
            
        Returns:
            Reasoning string
        """
        try:
            if "does not provide" in answer.lower():
                return "No specific information found in the document context"
            elif any(indicator in answer.lower() for indicator in ["section", "clause", "paragraph"]):
                return "Found explicit reference in document structure"
            elif any(indicator in answer.lower() for indicator in ["$", "%", "limit", "coverage"]):
                return "Found specific numerical or coverage information"
            else:
                return "Answer extracted from document context"
        except Exception:
            return "Answer generated from available context"
    
    async def batch_generate_answers(self, questions_and_contexts: list) -> list:
        """
        Generate answers for multiple questions in batch
        
        Args:
            questions_and_contexts: List of (question, context) tuples
            
        Returns:
            List of SimpleAnswerResult objects
        """
        try:
            logger.info(f"Batch generating {len(questions_and_contexts)} answers")
            
            tasks = [
                self.generate_answer(question, context)
                for question, context in questions_and_contexts
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Handle any exceptions in the results
            final_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    question = questions_and_contexts[i][0]
                    logger.error(f"Error in batch answer generation for question {i}: {str(result)}")
                    final_results.append(SimpleAnswerResult(
                        question=question,
                        answer="An error occurred while processing this question.",
                        confidence=0.0,
                        source_chunks=[],
                        reasoning=f"Error: {str(result)}"
                    ))
                else:
                    final_results.append(result)
            
            return final_results
            
        except Exception as e:
            logger.error(f"Error in batch answer generation: {str(e)}")
            raise
