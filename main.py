from fastapi import FastAPI, HTTPException, Depends, Request
from models import Base, Roupa, Fornecedor, Cliente, Pedido, ItensPedido
from database import engine, get_db
from crud import roupaRouter, fornecedorRouter, clienteRouter, pedidoRouter, itensPedidoRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
import logging
import json_log_formatter
import time
import datetime

app = FastAPI()

Base.metadata.create_all(bind=engine)

#crud
app.include_router(roupaRouter)
app.include_router(fornecedorRouter)
app.include_router(clienteRouter)
app.include_router(pedidoRouter)
app.include_router(itensPedidoRouter)

#quantidade de entidades
@app.get("/quantidade/roupas")
def get_quantidade_roupas(db: Session = Depends(get_db)):
    try:
        quantidade = db.query(Roupa).count()
        return {"quantidade": quantidade}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao contar as roupas.")

@app.get("/quantidade/fornecedores")
def get_quantidade_fornecedores(db: Session = Depends(get_db)):
    try:
        quantidade = db.query(Fornecedor).count()
        return {"quantidade": quantidade}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao contar os fornecedores.")
    
@app.get("/quantidade/clientes")
def get_quantidade_clientes(db: Session = Depends(get_db)):
    try:
        quantidade = db.query(Cliente).count()
        return {"quantidade": quantidade}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao contar os clientes.")    

@app.get("/quantidade/pedidos")
def get_quantidade_pedidos(db: Session = Depends(get_db)):
    try:
        quantidade = db.query(Pedido).count()
        return {"quantidade": quantidade}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao contar os pedidos.")
    
@app.get("/quantidade/itensPedidos")
def get_quantidade_itensPedidos(db: Session = Depends(get_db)):
    try:
        quantidade = db.query(ItensPedido).count()
        return {"quantidade": quantidade}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao contar os itens do Pedido.")

#gets paginados
@app.get("/roupas/paginadas/")
def get_roupas_paginadas(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    try:
        offset = (page - 1) * limit
        roupas = db.query(Roupa).offset(offset).limit(limit).all()
        total_roupas = db.query(func.count(Roupa.id)).scalar()
        total_paginas = (total_roupas + limit - 1) // limit

        return {
            "page": page,
            "limit": limit,
            "total_roupas": total_roupas,
            "total_paginas": total_paginas,
            "roupas": roupas
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao obter as roupas paginadas.")
    
@app.get("/fornecedores/paginados/")
def get_fornecedores_paginadas(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    try:
        offset = (page - 1) * limit
        fornecedores = db.query(Fornecedor).offset(offset).limit(limit).all()
        total_fornecedores = db.query(func.count(Fornecedor.id)).scalar()
        total_paginas = (total_fornecedores + limit - 1) // limit

        return {
            "page": page,
            "limit": limit,
            "total_fornecedores": total_fornecedores,
            "total_paginas": total_paginas,
            "fornecedores": fornecedores
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao obter os fornecedores paginados.")

@app.get("/clientes/paginados/")
def get_clientes_paginados(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    try:
        offset = (page - 1) * limit
        clientes = db.query(Cliente).offset(offset).limit(limit).all()
        total_clientes = db.query(func.count(Cliente.id)).scalar()
        total_paginas = (total_clientes + limit - 1) // limit

        return {
            "page": page,
            "limit": limit,
            "total_clientes": total_clientes,
            "total_paginas": total_paginas,
            "clientes": clientes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao obter os clientes paginados.")

@app.get("/pedidos/paginados/")
def get_pedidos_paginados(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    try:
        offset = (page - 1) * limit
        pedidos = db.query(Pedido).offset(offset).limit(limit).all()
        total_pedidos = db.query(func.count(Pedido.id)).scalar()
        total_paginas = (total_pedidos + limit - 1) // limit

        return {
            "page": page,
            "limit": limit,
            "total_clientes": total_pedidos,
            "total_paginas": total_paginas,
            "pedidos": pedidos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao obter os pedidos paginados.")

@app.get("/itensPedidos/paginados/")
def get_itensPedidos_paginados(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    try:
        offset = (page - 1) * limit
        itensPedidos = db.query(ItensPedido).offset(offset).limit(limit).all()
        total_itenspedidos = db.query(func.count(ItensPedido.id)).scalar()
        total_paginas = (total_itenspedidos + limit - 1) // limit

        return {
            "page": page,
            "limit": limit,
            "total_itensPedidos": total_itenspedidos,
            "total_paginas": total_paginas,
            "itensPedidos": itensPedidos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao obter os itens paginados.")
    
from typing import Optional

#filtros com optionals
@app.get("/roupas/filtrar/")
def filtrar_roupas(
    nome: Optional[str] = None,
    tamanho: Optional[str] = None,
    cor: Optional[str] = None,
    preco_min: Optional[float] = None,
    preco_max: Optional[float] = None,
    fornecedor_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Roupa)
        
        if nome:
            query = query.filter(Roupa.nome.ilike(f"%{nome}%"))
        if tamanho:
            query = query.filter(Roupa.tamanho == tamanho)
        if cor:
            query = query.filter(Roupa.cor.ilike(f"%{cor}%"))
        if preco_min is not None:
            query = query.filter(Roupa.preco >= preco_min)
        if preco_max is not None:
            query = query.filter(Roupa.preco <= preco_max)
        if fornecedor_id:
            query = query.filter(Roupa.fornecedor_id == fornecedor_id)
        
        roupas = query.all()

        return {"roupas": roupas}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao filtrar as roupas.")

@app.get("/fornecedores/filtrar/")
def filtrar_fornecedores(
    nome: Optional[str] = None,
    telefone: Optional[str] = None,
    email: Optional[str] = None,
    cidade: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Fornecedor)

        if nome:
            query = query.filter(Fornecedor.nome.ilike(f"%{nome}%"))
        if telefone:
            query = query.filter(Fornecedor.telefone.ilike(f"%{telefone}%"))
        if email:
            query = query.filter(Fornecedor.email.ilike(f"%{email}%"))
        if cidade:
            query = query.filter(Fornecedor.cidade.ilike(f"%{cidade}%"))

        fornecedores = query.all()
        return {"fornecedores": fornecedores}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao filtrar os fornecedores.")

@app.get("/clientes/filtrar/")
def filtrar_clientes(
    nome: Optional[str] = None,
    cpf: Optional[str] = None,
    telefone: Optional[str] = None,
    cidade: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Cliente)

        if nome:
            query = query.filter(Cliente.nome.ilike(f"%{nome}%"))
        if cpf:
            query = query.filter(Cliente.cpf.ilike(f"%{cpf}%"))
        if telefone:
            query = query.filter(Cliente.telefone.ilike(f"%{telefone}%"))

        clientes = query.all()
        return {"clientes": clientes}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao filtrar os clientes.")

@app.get("/pedidos/filtrar/")
def filtrar_pedidos(
    cliente_id: Optional[int] = None,
    status: Optional[str] = None,
    data_min: Optional[date] = None,
    data_max: Optional[date] = None,
    valor_min: Optional[float] = None,
    valor_max: Optional[float] = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Pedido)

        if cliente_id:
            query = query.filter(Pedido.cliente_id == cliente_id)
        if status:
            query = query.filter(Pedido.status.ilike(f"%{status}%"))
        if data_min:
            query = query.filter(Pedido.data >= data_min)
        if data_max:
            query = query.filter(Pedido.data <= data_max)
        if valor_min:
            query = query.filter(Pedido.valor_total >= valor_min)
        if valor_max:
            query = query.filter(Pedido.valor_total <= valor_max)

        pedidos = query.all()
        return {"pedidos": pedidos}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao filtrar os pedidos.")

@app.get("/itensPedido/filtrar/")
def filtrar_itens_pedido(
    pedido_id: Optional[int] = None,
    roupa_id: Optional[int] = None,
    quantidade_min: Optional[int] = None,
    quantidade_max: Optional[int] = None,
    preco_unitario_min: Optional[float] = None,
    preco_unitario_max: Optional[float] = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(ItensPedido)

        if pedido_id:
            query = query.filter(ItensPedido.pedido_id == pedido_id)
        if roupa_id:
            query = query.filter(ItensPedido.roupa_id == roupa_id)
        if quantidade_min:
            query = query.filter(ItensPedido.quantidade >= quantidade_min)
        if quantidade_max:
            query = query.filter(ItensPedido.quantidade <= quantidade_max)
        if preco_unitario_min:
            query = query.filter(ItensPedido.preco_unitario >= preco_unitario_min)
        if preco_unitario_max:
            query = query.filter(ItensPedido.preco_unitario <= preco_unitario_max)

        itens_pedido = query.all()
        return {"itensPedido": itens_pedido}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao filtrar os itens do pedido.")

#logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

logger = logging.getLogger(__name__)
logger.info("Aplicação iniciada")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fastapi")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Recebendo requisição: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Resposta enviada com status: {response.status_code}")
    return response

formatter = json_log_formatter.JSONFormatter()
json_handler = logging.FileHandler(filename='app.log')
json_handler.setFormatter(formatter)
logger.addHandler(json_handler)

logger.info("Início da aplicação", extra={"event": "startup"})

@app.middleware("http")
async def measure_execution_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Tempo de execução: {process_time} segundos")
    return response


#consultas com relacionamentos
@app.get("/fornecedores/{fornecedor_id}/roupas")
def listar_roupas_por_fornecedor(fornecedor_id: int, db: Session = Depends(get_db)):
    roupas = db.query(Roupa).filter(Roupa.fornecedor_id == fornecedor_id).all()
    return roupas

@app.get("/clientes/{cliente_id}/pedidos")
def listar_pedidos_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).filter(Pedido.cliente_id == cliente_id).all()
    return pedidos

@app.get("/pedidos/{pedido_id}/itens")
def listar_itens_por_pedido(pedido_id: int, db: Session = Depends(get_db)):
    itens = db.query(ItensPedido).filter(ItensPedido.pedido_id == pedido_id).all()
    return itens

@app.get("/roupas/busca/")
def buscar_roupas_por_nome(nome: str, db: Session = Depends(get_db)):
    roupas = db.query(Roupa).filter(Roupa.nome.ilike(f"%{nome}%")).all()
    return roupas

@app.get("/fornecedores/busca/")
def buscar_fornecedores_por_cidade(cidade: str, db: Session = Depends(get_db)):
    fornecedores = db.query(Fornecedor).filter(Fornecedor.cidade.ilike(f"%{cidade}%")).all()
    return fornecedores

@app.get("/pedidos/filtro/ano")
def filtrar_pedidos_por_ano(ano: int, db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).filter(Pedido.data.like(f"{ano}-%")).all()
    return pedidos

@app.get("/pedidos/filtro/intervalo")
def filtrar_pedidos_por_intervalo(data_inicio: str, data_fim: str, db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).filter(Pedido.data.between(data_inicio, data_fim)).all()
    return pedidos

@app.get("/fornecedores/roupas/contagem")
def contar_roupas_por_fornecedor(db: Session = Depends(get_db)):
    contagens = (
        db.query(Fornecedor.nome, func.count(Roupa.id).label("total_roupas"))
        .join(Roupa, Fornecedor.id == Roupa.fornecedor_id)
        .group_by(Fornecedor.nome)
        .all()
    )
    return contagens

@app.get("/pedidos/contagem/")
def contar_pedidos_por_status(db: Session = Depends(get_db)):
    contagens = (
        db.query(Pedido.status, func.count(Pedido.id).label("total_pedidos"))
        .group_by(Pedido.status)
        .all()
    )
    return contagens

@app.get("/roupas/ordenadas/")
def listar_roupas_ordenadas_por_preco(ordenacao: str = "asc", db: Session = Depends(get_db)):
    if ordenacao == "asc":
        roupas = db.query(Roupa).order_by(Roupa.preco.asc()).all()
    elif ordenacao == "desc":
        roupas = db.query(Roupa).order_by(Roupa.preco.desc()).all()
    else:
        raise HTTPException(status_code=400, detail="Ordenação inválida. Use 'asc' ou 'desc'.")
    return roupas

@app.get("/clientes/ordenados/")
def listar_clientes_ordenados_por_nome(ordenacao: str = "asc", db: Session = Depends(get_db)):
    if ordenacao == "asc":
        clientes = db.query(Cliente).order_by(Cliente.nome.asc()).all()
    elif ordenacao == "desc":
        clientes = db.query(Cliente).order_by(Cliente.nome.desc()).all()
    else:
        raise HTTPException(status_code=400, detail="Ordenação inválida. Use 'asc' ou 'desc'.")
    return clientes

@app.get("/pedidos/detalhados/")
def listar_pedidos_com_detalhes(db: Session = Depends(get_db)):
    pedidos = (
        db.query(Pedido, Cliente)
        .join(Cliente, Pedido.cliente_id == Cliente.id)
        .all()
    )
    resultado = []
    for pedido, cliente in pedidos:
        itens = (
            db.query(ItensPedido)
            .filter(ItensPedido.pedido_id == pedido.id)
            .all()
        )
        resultado.append(
            {
                "pedido_id": pedido.id,
                "data": pedido.data,
                "status": pedido.status,
                "cliente": cliente.nome,
                "itens": [
                    {
                        "roupa_id": item.roupa_id,
                        "quantidade": item.quantidade,
                        "preco_unitario": item.preco_unitario,
                    }
                    for item in itens
                ],
            }
        )
    return resultado

@app.get("/roupas/fornecedores/")
def listar_roupas_com_fornecedores(db: Session = Depends(get_db)):
    roupas = (
        db.query(Roupa, Fornecedor)
        .join(Fornecedor, Roupa.fornecedor_id == Fornecedor.id)
        .all()
    )
    resultado = [
        {
            "roupa_id": roupa.id,
            "nome": roupa.nome,
            "fornecedor": fornecedor.nome,
        }
        for roupa, fornecedor in roupas
    ]
    return resultado