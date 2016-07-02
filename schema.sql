DROP TABLE IF EXISTS entries;
DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
  id         TEXT PRIMARY KEY,
  content    TEXT NOT NULL,
  caret_pos  INT  NOT NULL,
  scroll_pos INT  NOT NULL,
  font_size  INT  NOT NULL
);
