SELECT 
    c.name AS customer_name,
    p.name AS product_name,
    p.price AS price,
    o.qty AS qty,
    pay.amount AS total_amount,
    pay.status AS payment_status,
    s.shipment_status AS shipment_status
FROM 
    orders o
LEFT JOIN 
    customers c ON o.customer_id = c.id
LEFT JOIN 
    products p ON o.product_id = p.id
LEFT JOIN 
    payments pay ON o.order_id = pay.order_id
LEFT JOIN 
    shipments s ON o.order_id = s.order_id
ORDER BY 
    o.order_id;

