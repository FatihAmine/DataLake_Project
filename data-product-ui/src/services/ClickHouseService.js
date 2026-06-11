export const ClickHouseService = {
  /**
   * Executes a query against the ClickHouse instance via the configured Vite proxy
   */
  async executeQuery(query) {
    try {
      const response = await fetch('/api/clickhouse', {
        method: 'POST',
        headers: {
          'Content-Type': 'text/plain',
          'Authorization': 'Basic ' + btoa('default:clickhouse')
        },
        body: `${query} FORMAT JSON`
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`ClickHouse Error: ${response.status} - ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Failed to execute query:', error);
      throw error;
    }
  },

  /**
   * Ping ClickHouse to check connection
   */
  async ping() {
    try {
      const result = await this.executeQuery('SELECT 1 as is_alive');
      return result.data && result.data.length > 0;
    } catch (error) {
      return false;
    }
  },

  /**
   * Get Overall Counters from daily_sales view
   */
  async getOverallMetrics() {
    try {
      const result = await this.executeQuery(`
        SELECT 
          sum(total_units) as total_orders,
          sum(total_sales) as total_revenue,
          count() as total_lines
        FROM ecommerce_product.daily_sales
      `);
      return result.data[0];
    } catch (e) {
      return { total_lines: 0, total_revenue: 0, total_orders: 0 };
    }
  },

  /**
   * Get Sales Per Day from daily_sales view
   */
  async getSalesPerDay() {
    try {
      const result = await this.executeQuery(`
        SELECT 
          toString(order_date) as date,
          total_sales as revenue
        FROM ecommerce_product.daily_sales
        ORDER BY order_date ASC
        LIMIT 30
      `);
      return result.data;
    } catch (e) {
      return [];
    }
  },

  /**
   * Get Sales by Category from sales_by_category view
   */
  async getSalesByCategory() {
    try {
      const result = await this.executeQuery(`
        SELECT 
          category,
          total_sales as revenue
        FROM ecommerce_product.sales_by_category
        ORDER BY total_sales DESC
        LIMIT 10
      `);
      return result.data;
    } catch (e) {
      return [];
    }
  },

  /**
   * Get Top Products from top_products view
   */
  async getTopProducts() {
    try {
      const result = await this.executeQuery(`
        SELECT 
          product,
          total_units,
          total_sales as amount
        FROM ecommerce_product.top_products
        ORDER BY total_sales DESC
        LIMIT 10
      `);
      return result.data;
    } catch (e) {
      return [];
    }
  }
};
