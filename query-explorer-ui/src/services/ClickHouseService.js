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
        body: query
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`ClickHouse Error: ${response.status} - ${errorText.trim()}`);
      }

      const text = await response.text();
      try {
        return JSON.parse(text);
      } catch (e) {
        return text;
      }
    } catch (error) {
      console.error('Failed to execute ClickHouse query:', error);
      throw error;
    }
  }
};
