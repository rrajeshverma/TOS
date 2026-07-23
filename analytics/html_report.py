class HTMLReport:
    def generate(self, summary):
        return f"""
<html>
<head>
<title>Backtest Report</title>
</head>
<body>
<h1>Backtest Summary</h1>

<table border="1">
<tr><td>Initial Capital</td><td>{summary["initial_capital"]}</td></tr>
<tr><td>Final Capital</td><td>{summary["final_capital"]}</td></tr>
<tr><td>Net Profit</td><td>{summary["net_profit"]}</td></tr>
<tr><td>Win Rate</td><td>{summary["win_rate"]}</td></tr>
</table>

</body>
</html>
"""
