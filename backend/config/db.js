const { Pool } = require("pg"); //handles the connection between psql and node

const pool = new Pool({
  user: "postgres",
  password: "MSUCOLT!",
  host: "localhost",
  port: 5432,
  database: "Discs",
});

module.exports = {
  query: (text, params) => pool.query(text, params),
};
