-- Running count of number of stocks in the dataset, ordered by date

select
    distinct date,
    count(*) over(order by date) as running_count
from sentiment_analysis
order by date;