package com.br.biblioteca.dao;

import com.br.biblioteca.log.Log;
import com.br.biblioteca.model.Autor;

import javax.persistence.EntityManager;
import java.io.IOException;
import java.util.List;

public class AutorDAO {
    private EntityManager em;

    //Criando a instãncia do Logger
    Log meuLogger = new Log("Log.txt");

    //Contrutor por atribuir o EntityManager vindo como parâmetro para o atributo em da classe local
    public AutorDAO(EntityManager em) throws IOException {
        this.em = em;
    }

    //Método responsável por cadastrar um autor no banco de dados
    public void cadastrar(Autor autor) {
        this.em.persist(autor);
        System.out.println("\nO autor '" + autor.getNome() + "' foi criada com sucesso!\n");
        meuLogger.logger.info("\nO autor '" + autor.getNome() + "' foi criada na base de dados!\n");
    }

}
