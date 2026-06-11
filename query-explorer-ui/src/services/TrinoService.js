export const TrinoService = {
  /**
   * Execute a query against Trino and poll until complete.
   * @param {string} query The SQL query to execute
   */
  async executeQuery(query) {
    try {
      let response = await fetch('/v1/statement', {
        method: 'POST',
        headers: {
          'X-Trino-User': 'admin',
          'Content-Type': 'text/plain'
        },
        body: query
      });

      if (!response.ok) {
        throw new Error(`Trino Error: ${response.statusText}`);
      }

      let result = await response.json();
      let columns = result.columns || [];
      let data = result.data || [];

      // Poll nextUri until the query is fully processed
      while (result.nextUri) {
        // We use relative path for the proxy since Trino returns full URI (e.g., http://localhost:8080/v1/statement/...)
        const nextPath = new URL(result.nextUri).pathname + new URL(result.nextUri).search;
        
        // Wait a little before polling to avoid spamming
        await new Promise(r => setTimeout(r, 200));

        response = await fetch(nextPath, {
          method: 'GET',
          headers: {
            'X-Trino-User': 'admin'
          }
        });

        if (!response.ok) {
          throw new Error(`Trino Polling Error: ${response.statusText}`);
        }

        result = await response.json();
        
        if (result.error) {
          throw new Error(result.error.message);
        }

        if (result.columns && columns.length === 0) {
          columns = result.columns;
        }

        if (result.data) {
          data = data.concat(result.data);
        }
      }

      return { columns, data };
    } catch (error) {
      console.error('Trino Query failed:', error);
      throw error;
    }
  },

  async getCatalogs() {
    const res = await this.executeQuery('SHOW CATALOGS');
    return res.data ? res.data.map(row => row[0]).filter(c => c !== 'system') : [];
  },

  async getSchemas(catalog) {
    const res = await this.executeQuery(`SHOW SCHEMAS IN ${catalog}`);
    return res.data ? res.data.map(row => row[0]).filter(s => s !== 'information_schema') : [];
  },

  async getTables(catalog, schema) {
    const res = await this.executeQuery(`SHOW TABLES IN ${catalog}.${schema}`);
    return res.data ? res.data.map(row => row[0]) : [];
  }
};
