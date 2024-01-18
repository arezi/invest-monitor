

from sqlalchemy.sql import text


from .models import db, to_dict




class OperationRepository:

    def list_active(self, on_date):
        sql = """
        select d.ticker_amount, d.ticker_last_operation, o.*
            from operation o,
                (select ticker, 
                        sum(buy) - sum(sell) AS ticker_amount,
                        max(date) AS ticker_last_operation 
                   from operation 
                  where date <= '%s'
                  group by ticker) as d 
            where o.ticker = d.ticker 
            and o.buy > 0 
            and d.ticker_amount > 0 
            and o.date <= '%s'
            order by d.ticker_last_operation desc, o.ticker, o.date desc
        """%(on_date, on_date)
        rs = db.session.execute(text(sql))
        return to_dict(rs)


    def sum_sold_current_month(self, stocks_exchange):
        
        # stocks_exchange still does'nt work (only BOVESPA)

        sql = """
        select SUM(sell * price) sum_sold
        from operation 
        where sell >= 0
        and ticker not like '%11' -- desconsiderar FII e ETLs
        and date >= strftime('%Y-%m', 'now') and date < strftime('%Y-%m', 'now', '+1 month') -- current month
        """
        rs = db.session.execute(text(sql))
        sum = rs.first().sum_sold
        return sum if sum is not None else 0 


