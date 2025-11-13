"""
TrustNet 2.0 - Model Training Script
Fine-tune RoBERTa on fake news detection dataset
"""

import torch
from torch.utils.data import Dataset, DataLoader
from transformers import RobertaTokenizer, RobertaForSequenceClassification, AdamW
from sklearn.model_selection import train_test_split
import pandas as pd
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FakeNewsDataset(Dataset):
    """Dataset for fake news detection"""
    
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }


def load_dataset(dataset_path):
    """
    Load fake news dataset
    
    Expected format:
    CSV with columns: 'text', 'label' (0=real, 1=fake)
    
    Popular datasets:
    1. FakeNewsNet: https://github.com/KaiDMML/FakeNewsNet
    2. LIAR: https://www.cs.ucsb.edu/~william/data/liar_dataset.zip
    3. ISOT: https://www.uvic.ca/engineering/ece/isot/datasets/fake-news/index.php
    """
    
    logger.info(f"Loading dataset from {dataset_path}")
    
    # Example: Load CSV
    df = pd.read_csv(dataset_path)
    
    # Assume columns: 'text', 'label'
    texts = df['text'].tolist()
    labels = df['label'].tolist()
    
    logger.info(f"Loaded {len(texts)} examples")
    logger.info(f"Real news: {labels.count(0)}, Fake news: {labels.count(1)}")
    
    return texts, labels


def train_model(
    dataset_path,
    model_name='roberta-base',
    batch_size=16,
    epochs=3,
    learning_rate=2e-5,
    output_dir='./models/roberta-fakenews'
):
    """Train RoBERTa for fake news detection"""
    
    # Setup device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info(f"Using device: {device}")
    
    # Load dataset
    texts, labels = load_dataset(dataset_path)
    
    # Split dataset
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    logger.info(f"Training set: {len(train_texts)} examples")
    logger.info(f"Validation set: {len(val_texts)} examples")
    
    # Load tokenizer and model
    logger.info("Loading model...")
    tokenizer = RobertaTokenizer.from_pretrained(model_name)
    model = RobertaForSequenceClassification.from_pretrained(
        model_name,
        num_labels=2
    ).to(device)
    
    # Create datasets
    train_dataset = FakeNewsDataset(train_texts, train_labels, tokenizer)
    val_dataset = FakeNewsDataset(val_texts, val_labels, tokenizer)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)
    
    # Setup optimizer
    optimizer = AdamW(model.parameters(), lr=learning_rate)
    
    # Training loop
    logger.info("Starting training...")
    best_val_acc = 0.0
    
    for epoch in range(epochs):
        logger.info(f"\nEpoch {epoch + 1}/{epochs}")
        
        # Training
        model.train()
        train_loss = 0
        train_correct = 0
        train_total = 0
        
        for batch in tqdm(train_loader, desc="Training"):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            optimizer.zero_grad()
            
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            
            predictions = torch.argmax(outputs.logits, dim=1)
            train_correct += (predictions == labels).sum().item()
            train_total += labels.size(0)
        
        train_acc = train_correct / train_total
        avg_train_loss = train_loss / len(train_loader)
        
        # Validation
        model.eval()
        val_loss = 0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for batch in tqdm(val_loader, desc="Validation"):
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['labels'].to(device)
                
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
                
                val_loss += outputs.loss.item()
                
                predictions = torch.argmax(outputs.logits, dim=1)
                val_correct += (predictions == labels).sum().item()
                val_total += labels.size(0)
        
        val_acc = val_correct / val_total
        avg_val_loss = val_loss / len(val_loader)
        
        logger.info(f"Train Loss: {avg_train_loss:.4f}, Train Acc: {train_acc:.4f}")
        logger.info(f"Val Loss: {avg_val_loss:.4f}, Val Acc: {val_acc:.4f}")
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            logger.info(f"Saving best model (acc: {val_acc:.4f})")
            model.save_pretrained(output_dir)
            tokenizer.save_pretrained(output_dir)
    
    logger.info(f"\nTraining complete! Best validation accuracy: {best_val_acc:.4f}")
    logger.info(f"Model saved to: {output_dir}")
    
    return model, tokenizer


def test_model(model_path, test_text):
    """Test the trained model"""
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    tokenizer = RobertaTokenizer.from_pretrained(model_path)
    model = RobertaForSequenceClassification.from_pretrained(model_path).to(device)
    model.eval()
    
    encoding = tokenizer(
        test_text,
        truncation=True,
        padding='max_length',
        max_length=512,
        return_tensors='pt'
    )
    
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)
    
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        predictions = torch.softmax(outputs.logits, dim=1)
        fake_prob = predictions[0][1].item()
    
    return {
        'fake_probability': fake_prob,
        'classification': 'FAKE' if fake_prob > 0.5 else 'REAL',
        'confidence': max(predictions[0]).item()
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Train TrustNet fake news detector')
    parser.add_argument('--dataset', type=str, required=True, help='Path to dataset CSV')
    parser.add_argument('--epochs', type=int, default=3, help='Number of epochs')
    parser.add_argument('--batch-size', type=int, default=16, help='Batch size')
    parser.add_argument('--lr', type=float, default=2e-5, help='Learning rate')
    parser.add_argument('--output', type=str, default='./models/roberta-fakenews', help='Output directory')
    
    args = parser.parse_args()
    
    # Train model
    model, tokenizer = train_model(
        dataset_path=args.dataset,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        output_dir=args.output
    )
    
    # Test with example
    print("\n" + "="*80)
    print("Testing trained model:")
    print("="*80)
    
    test_cases = [
        "Scientists have discovered a new planet that could support life.",
        "BREAKING: Doctors hate this one weird trick to lose weight instantly!",
        "President announces new economic policy to boost job growth."
    ]
    
    for text in test_cases:
        result = test_model(args.output, text)
        print(f"\nText: {text[:60]}...")
        print(f"Classification: {result['classification']}")
        print(f"Fake Probability: {result['fake_probability']:.2%}")
        print(f"Confidence: {result['confidence']:.2%}")
