/* TODO: Delete this - delete and create sql schema for testing */
drop schema public cascade;
create schema public;

/* Records */

create table chunks(
  id								serial primary key,
	url								varchar not null,
	text							varchar not null,
	paragraph_count		int not null,
	chunk_count				int not null,
	embedding					bytea,
	constraint chunck_unique unique (url, paragraph_count, chunk_count),
	constraint text_unique unique (text)
);