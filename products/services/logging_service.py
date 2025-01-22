# products/services/logging_service.py 주인공
from django.conf import settings
from datetime import datetime
from typing import Dict, Any ,Optional

class LoggingService:
    @staticmethod
    def log_product_view(user_id: Optional[int], product_id: int, metadata: Dict[str, Any] = None) -> None:
        """상품 조회 로그를 기록합니다."""
        log_data = {
            'user_id': str(user_id) if user_id else None,
            'product_id': str(product_id),
            'action': 'view_product',
            'timestamp': datetime.now(),
            'metadata': metadata or {}
        }
        settings.MONGODB_DATABASE.product_logs.insert_one(log_data)    #여기 함수 데이터가 중요. 수집

    @staticmethod
    def get_product_view_stats(product_id: int) -> Dict[str, Any]:
        """상품 조회 통계를 조회합니다."""
        pipeline = [
            {'$match': {'product_id': str(product_id)}},
            {'$group': {
                '_id': None,
                'view_count': {'$sum': 1},
                'unique_users': {'$addToSet': '$user_id'}
            }}
        ]
        result = list(settings.MONGODB_DATABASE.product_logs.aggregate(pipeline))

        if result:
            stats = result[0]
            return {
                'total_views': stats['view_count'],
                'unique_viewers': len(stats['unique_users']) - (1 if None in stats['unique_users'] else 0)
            }
        return {'total_views': 0, 'unique_viewers': 0}
