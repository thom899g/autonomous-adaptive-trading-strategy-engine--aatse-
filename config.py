"""
Configuration management for AATSE system.
Centralizes all configurable parameters with type safety and validation.
"""
import os
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ExchangeConfig:
    """Configuration for exchange connections"""
    name: str
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    sandbox: bool = True
    rate_limit: int = 1000
    timeout: int = 30


@dataclass
class StrategyConfig:
    """Configuration for strategy parameters"""
    population_size: int = 100
    generations: int = 50
    mutation_rate: float = 0.1
    crossover_rate: float = 0.7
    elite_count: int = 5
    max_strategy_length: int = 10


@dataclass
class RiskConfig:
    """Configuration for risk management"""
    max_position_size: float = 0.1  # 10% of portfolio
    max_daily_loss: float = 0.02  # 2% daily loss limit
    max_drawdown: float = 0.1  # 10% max drawdown
    stop_loss_pct: float = 0.02  # 2% stop loss
    take_profit_pct: float = 0.05  # 5% take profit


@dataclass
class RLConfig:
    """Configuration for reinforcement learning"""
    learning_rate: float = 0.001
    discount_factor: float = 0.99
    exploration_rate: float = 0.1
    batch_size: int = 32
    memory_size: int = 10000


class Config:
    """Main configuration class with validation"""
    
    def __init__(self):
        # Default configurations
        self.exchange = ExchangeConfig(name="binance")
        self.strategy = StrategyConfig()
        self.risk = RiskConfig()
        self.rl = RLConfig()
        
        # System parameters
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.data_refresh_interval: int = 60  # seconds
        self.backtest_lookback_days: int = 365
        self.realtime_trading: bool = False
        
        # Firebase configuration
        self.firebase_project_id: Optional[str] = os.getenv("FIREBASE_PROJECT_ID")
        self.firebase_credentials_path: Optional[str] = os.getenv("FIREBASE_CREDENTIALS")
        
        # Validate critical configurations
        self._validate()
    
    def _validate(self) -> None:
        """Validate configuration values"""
        errors = []
        
        if not self.firebase_project_id:
            errors.append("FIREBASE_PROJECT_ID environment variable not set")
        
        if not self.firebase_credentials_path:
            errors.append("FIREBASE_CREDENTIALS environment variable not set")
        
        if errors:
            error_msg = "Configuration errors:\n" + "\n".join(errors)
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info("Configuration validated successfully")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for serialization"""
        return {
            "exchange": {
                "name": self.exchange.name,
                "sandbox": self.exchange.sandbox,
                "rate_limit": self.exchange.rate_limit
            },
            "strategy": {
                "population_size": self.strategy.population_size,
                "generations": self.strategy.generations
            },
            "risk": {
                "max_position_size": self.risk.max_position_size,
                "max_daily_loss": self.risk.max_daily_loss
            }
        }


# Global config instance
config = Config()