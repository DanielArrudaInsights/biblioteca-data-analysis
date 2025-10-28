create table Autores(
	ID_autor serial primary key,
	Nome_do_autor varchar (45) unique not null,
	Nacionalidade varchar (30)
);

create table Status_leitores (
	ID_status serial primary key,
	Nome_do_status varchar (15) not null unique
);
create table Livros(
	ID serial primary key,
	ID_autor int not null,
	ID_status int not null,
	ISBN varchar (20),
	titulo varchar (50),
	Data_de_Publicacao date,
	Numero_de_Paginas smallint not null,
	genero varchar (30) not null,
	data_inicio_leitura date,
	data_fim_leitura date,
	data_aquisicao date not null,
	foreign key (ID_autor) references Autores (ID_autor),
	foreign key (ID_status) references Status_leitores (ID_status)
);
