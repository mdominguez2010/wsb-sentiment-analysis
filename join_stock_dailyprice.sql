SELECT
	s.symbol,
	dp.*
from stock s join daily_price dp
	on s.id = dp.stock_id
