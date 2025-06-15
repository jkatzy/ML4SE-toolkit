SELECT
    c.CustomerName,
    c.Country,
    SUM(p.Price * o.Quantity) AS TotalSpentOnElectronics
FROM
    Customers c
JOIN
    Orders o ON c.CustomerID = o.CustomerID
JOIN
    Products p ON o.ProductID = p.ProductID
WHERE
    p.Category = 'Electronics'
GROUP BY
    c.CustomerID, c.CustomerName, c.Country
HAVING
    SUM(p.Price * o.Quantity) > 0 
ORDER BY
    TotalSpentOnElectronics DESC;
