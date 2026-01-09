"""Bill analysis utilities for anomaly detection"""
from typing import List, Dict, Any
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


# Procedure benchmarks for price comparison
PROCEDURE_BENCHMARKS = {
    "99213": 150,
    "99214": 200,
    "36415": 25,
    "80053": 50,
    "85025": 30,
    "93000": 100,
    "45378": 2000,
    "27447": 15000,
    "27130": 20000,
    "99221": 500,
    "99232": 400,
    "99284": 800,
}


class BillAnalyzer:
    """Analyze medical bills for errors and anomalies"""
    
    def __init__(self):
        self.benchmarks = PROCEDURE_BENCHMARKS
    
    def analyze_bill(self, line_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze bill line items for anomalies
        
        Args:
            line_items: List of bill line items with code, date, price, description
        
        Returns:
            Dictionary with issues found and estimated savings
        """
        issues = []
        total_savings = 0.0
        
        # Check 1: Duplicate charges same day
        duplicate_issues = self._check_duplicate_charges(line_items)
        issues.extend(duplicate_issues)
        total_savings += sum(issue.get('estimate_savings', 0) for issue in duplicate_issues)
        
        # Check 2: Overpriced items
        overpriced_issues = self._check_overpriced_items(line_items)
        issues.extend(overpriced_issues)
        total_savings += sum(issue.get('estimate_savings', 0) for issue in overpriced_issues)
        
        # Check 3: Impossible procedure combinations
        combo_issues = self._check_risky_combinations(line_items)
        issues.extend(combo_issues)
        
        # Check 4: Unbundled charges
        unbundled_issues = self._check_unbundled_charges(line_items)
        issues.extend(unbundled_issues)
        total_savings += sum(issue.get('estimate_savings', 0) for issue in unbundled_issues)
        
        # Check 5: Date inconsistencies
        date_issues = self._check_date_inconsistencies(line_items)
        issues.extend(date_issues)
        
        return {
            "issues": issues,
            "total_issues": len(issues),
            "total_savings": round(total_savings, 2),
            "high_severity_count": len([i for i in issues if i.get('severity') == 'high']),
            "medium_severity_count": len([i for i in issues if i.get('severity') == 'medium']),
            "low_severity_count": len([i for i in issues if i.get('severity') == 'low'])
        }
    
    def _check_duplicate_charges(self, line_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for duplicate charges on the same day"""
        issues = []
        codes_per_day = defaultdict(list)
        
        for item in line_items:
            date = item.get('date', '')
            code = item.get('code', '')
            codes_per_day[date].append((code, item))
        
        for date, code_items in codes_per_day.items():
            code_counts = defaultdict(list)
            for code, item in code_items:
                code_counts[code].append(item)
            
            for code, items in code_counts.items():
                if len(items) > 1:
                    # Duplicate found
                    total_price = sum(item.get('price', 0) for item in items)
                    savings = items[0].get('price', 0) * (len(items) - 1) * 0.9  # Assume 90% recoverable
                    
                    issues.append({
                        'type': 'duplicate_charge',
                        'severity': 'high',
                        'description': f"Procedure code {code} appears {len(items)} times on {date}",
                        'line_items': [item.get('description', '') for item in items],
                        'estimate_savings': savings,
                        'date': date
                    })
        
        return issues
    
    def _check_overpriced_items(self, line_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for items priced significantly above benchmark"""
        issues = []
        markup_threshold = 1.3  # 30% above benchmark
        
        for item in line_items:
            code = item.get('code', '')
            price = item.get('price', 0)
            benchmark = self.benchmarks.get(code, None)
            
            if benchmark and price > benchmark * markup_threshold:
                overcharge = price - benchmark
                savings = overcharge * 0.5  # Assume 50% recoverable
                
                issues.append({
                    'type': 'overpriced',
                    'severity': 'medium',
                    'description': f"Procedure {code} charged ${price:.2f}, benchmark is ${benchmark:.2f}",
                    'code': code,
                    'charged_price': price,
                    'benchmark_price': benchmark,
                    'overcharge': round(overcharge, 2),
                    'estimate_savings': savings
                })
        
        return issues
    
    def _check_risky_combinations(self, line_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for impossible or risky procedure combinations"""
        issues = []
        
        # Define risky combinations (simplified)
        risky_combos = [
            (['99213', '99214'], 'Same-day office visits at different levels'),
            (['93000', '93010'], 'Multiple EKGs same day without justification'),
        ]
        
        codes = [item.get('code', '') for item in line_items]
        dates = [item.get('date', '') for item in line_items]
        
        for combo_codes, description in risky_combos:
            if all(code in codes for code in combo_codes):
                # Check if on same date
                combo_items = [item for item in line_items if item.get('code') in combo_codes]
                if len(set(item.get('date') for item in combo_items)) == 1:
                    issues.append({
                        'type': 'risky_combination',
                        'severity': 'medium',
                        'description': description,
                        'codes': combo_codes,
                        'estimate_savings': 0  # Requires review, not automatic savings
                    })
        
        return issues
    
    def _check_unbundled_charges(self, line_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for unbundled charges (charges that should be bundled)"""
        issues = []
        
        # Simplified unbundling detection
        # In production, use comprehensive CPT bundling rules
        
        return issues
    
    def _check_date_inconsistencies(self, line_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for date inconsistencies"""
        issues = []
        
        # Check for future dates
        from datetime import datetime
        today = datetime.now().date()
        
        for item in line_items:
            date_str = item.get('date', '')
            try:
                item_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                if item_date > today:
                    issues.append({
                        'type': 'future_date',
                        'severity': 'high',
                        'description': f"Charge dated {date_str} is in the future",
                        'date': date_str,
                        'estimate_savings': 0
                    })
            except:
                pass
        
        return issues


# Global bill analyzer instance
bill_analyzer = BillAnalyzer()

