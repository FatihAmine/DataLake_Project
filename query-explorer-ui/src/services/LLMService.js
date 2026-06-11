export class LLMService {
  static async generateSQL(apiKey, schemaContext, userQuery) {
    if (!apiKey) {
      throw new Error("API Key is required to use the AI Chat feature.");
    }

    const systemPrompt = `You are a helpful data analyst AI assistant for Trino (Presto).
You help the user query and understand their data.
Below is the schema context for the available tables in Trino:

${schemaContext}

Important Instructions:
1. You can chat normally with the user.
2. If the user asks a question that requires querying the database, generate the necessary Trino SQL query.
3. ALWAYS wrap your SQL query in a markdown code block like this:
\`\`\`sql
SELECT * FROM catalog.schema.table;
\`\`\`
4. Ensure the query uses fully qualified table names (catalog.schema.table).`;

    const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: "google/gemini-2.5-pro",
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: userQuery }
        ],
        temperature: 0.1,
        max_tokens: 1024
      })
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(err.error?.message || "Failed to communicate with LLM API.");
    }

    const data = await response.json();
    return data.choices[0].message.content.trim();
  }
}
