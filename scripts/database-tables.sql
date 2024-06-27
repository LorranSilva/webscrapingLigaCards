CREATE TABLE game (
  id SERIAL PRIMARY KEY NOT NULL,
  name VARCHAR(70),
  acronym VARCHAR(10),
  release_date DATE,
  description TEXT
);

CREATE TABLE collection (
	id SERIAL PRIMARY KEY NOT NULL,
  game_id INT UNIQUE,
	name VARCHAR(150),
	acronym VARCHAR(15),
	cards_quantity integer,
	lowest_price decimal(13,2),
	average_price decimal(13,2),
  highest_price decimal(13,2),
  FOREIGN KEY (game_id) REFERENCES game (id) ON DELETE CASCADE
);
ALTER TABLE collection DROP CONSTRAINT collection_game_id_key;

CREATE TABLE card (
  id SERIAL PRIMARY KEY NOT NULL,
  collection_id INT,
  lowest_price DECIMAL(13, 2),
  highest_price DECIMAL(13, 2),
  name_EN VARCHAR(200),
  name_PT VARCHAR(200),
  FOREIGN KEY (collection_id) REFERENCES collection (id) ON DELETE CASCADE
);

INSERT INTO game(name, acronym, release_date, description) VALUES('Pokemon TCG', 'ptcg', '1996-10-20', 'Pokémon Trading Card Game, ou Pokémon Estampas Ilustradas no Brasil, é um jogo de cartas colecionáveis baseadas na franquia japonesa Pokémon. Publicado pela primeira vez em outubro de 1996, pela Media Factory, no Japão.');
INSERT INTO game(name, acronym, release_date, description) VALUES('Yu-Gi-Oh! Trading Card Game', 'ygo', '2002-03-01', 'O Yu-Gi-Oh! Trading Card Game é um jogo de cartas colecionáveis ​​desenvolvido e publicado pela Konami. É baseado no jogo fictício de Duel Monsters criado pelo artista de mangá Kazuki Takahashi, que aparece em partes da franquia de mangá Yu-Gi-Oh!');
INSERT INTO game(name, acronym, release_date, description) VALUES('Magic: The Gathering', 'mtg', '1993-08-05', 'Magic: the Gathering, M:TG, MTG ou simplesmente Magic, é um jogo de cartas colecionáveis criado por Richard Garfield, no qual os jogadores utilizam um baralho de cartas construído de acordo com o seu modo individual de jogo para tentar vencer o baralho adversário.');