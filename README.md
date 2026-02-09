# Pedidos Veloz – Plataforma de Pedidos em Microsserviços

Este repositório apresenta a implementação de uma plataforma de pedidos baseada em **arquitetura de microsserviços**, construída com **Docker**, **Docker Compose** e **Kubernetes**, seguindo princípios *cloud-native* e boas práticas de **DevOps**.

O projeto foi desenvolvido como resposta ao desafio de modernização da aplicação da empresa fictícia **Loja Veloz**, que enfrentava dificuldades de escalabilidade, indisponibilidade durante deploys e baixa observabilidade entre serviços.

---

## 📑 Sumário

- [Visão geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Ambiente local com Docker Compose](#ambiente-local-com-docker-compose)
- [Execução no Kubernetes (Minikube)](#execução-no-kubernetes-minikube)
- [Testes e validação](#testes-e-validação)
- [CI/CD](#cicd)
- [Observabilidade](#observabilidade)
- [Escalabilidade](#escalabilidade)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Troubleshooting](#troubleshooting)
- [Considerações finais](#considerações-finais)

---

## Visão geral

A aplicação **Pedidos Veloz** é composta por múltiplos serviços independentes que se comunicam via HTTP, permitindo evolução desacoplada, escalabilidade seletiva e melhor isolamento de falhas.

### Fluxo principal

1. O cliente acessa a aplicação via **API Gateway**
2. O Gateway orquestra chamadas para:
   - Serviço de Pedidos
   - Serviço de Pagamentos
   - Serviço de Estoque
3. O serviço de Pedidos persiste dados em um banco **PostgreSQL**

O projeto cobre desde o **ambiente local reproduzível** até a **orquestração em Kubernetes**, com foco em práticas de produção.

---

## Arquitetura

A arquitetura segue o padrão clássico de microsserviços:

- **Gateway**: ponto único de entrada (reverse proxy / API Gateway)
- **Pedidos**: criação e consulta de pedidos
- **Pagamentos**: simulação de processamento de pagamentos
- **Estoque**: controle e reserva de itens
- **PostgreSQL**: persistência de dados

### Características dos serviços

Cada serviço é:

- Stateless
- Conteinerizado individualmente
- Exposto via HTTP
- Configurado via variáveis de ambiente (12-Factor App)

---

## Ambiente local com Docker Compose

O ambiente de desenvolvimento local é definido no arquivo `docker-compose.yml`, permitindo subir toda a stack com um único comando.

### Pré-requisitos

- Docker
- Docker Compose

### Subindo o ambiente

```bash
docker compose up --build
```

### Acesso aos serviços

- **Gateway**: <http://localhost:8080>

#### Portas internas

| Serviço       | Porta |
|--------------|-------|
| Gateway      | 5000  |
| Pedidos      | 5000  |
| Pagamentos   | 5000  |
| Estoque      | 5000  |
| PostgreSQL   | 5432  |

> O banco de dados utiliza volume persistente, garantindo que os dados não sejam perdidos entre reinícios.

---

## Execução no Kubernetes (Minikube)

O ambiente Kubernetes apresentado utiliza o **Minikube**, com o objetivo de simular práticas de produção em um **cluster local e controlado**.

Os serviços foram implantados utilizando manifests Kubernetes, permitindo validar conceitos como orquestração, isolamento de workloads, configuração por ambiente e exposição de serviços de forma padronizada.

### Componentes utilizados

- Deployments
- Services (ClusterIP)
- ConfigMaps e Secrets
- Ingress Controller (NGINX)
- Ingress com roteamento por path

### Ingress

O acesso externo é feito via domínio local:

```
pedidos-veloz.local
```

#### Exemplos de endpoints

```bash
curl http://pedidos-veloz.local/pedidos/health
curl http://pedidos-veloz.local/pagamentos/health
curl http://pedidos-veloz.local/estoque/health
```

O roteamento é feito pelo **Ingress NGINX**, direcionando os paths para o Gateway.

---

## Testes e validação

Cada serviço expõe um endpoint de saúde (`/health`) utilizado para validação de funcionamento.

Esses endpoints podem ser usados para:

- Testes manuais
- Readiness probes
- Validação após deploy

### Exemplo

```bash
curl http://pedidos-veloz.local/pedidos/health
```

---

## CI/CD

O projeto inclui uma proposta de **pipeline de CI/CD**, utilizando GitHub Actions, com foco em automatizar o processo de build, versionamento e publicação das imagens Docker.

A implementação apresentada representa um **MVP funcional de pipeline**, servindo como base para evolução conforme a maturidade do time e do ambiente.

O pipeline contempla as seguintes etapas:

- Build das imagens Docker
- Versionamento
- Publicação em registry
- Execução de testes básicos
- Uso seguro de secrets no pipeline

Essa estrutura permite a evolução gradual do processo de entrega contínua, acompanhando o crescimento da aplicação e da infraestrutura.

---

## Observabilidade

A observabilidade da aplicação foi desenhada seguindo princípios *cloud-native*, com foco em padronização e compatibilidade com ferramentas amplamente adotadas no ecossistema Kubernetes.

Nesta etapa do projeto, a observabilidade é apresentada de forma **conceitual e arquitetural**, preparando o sistema para futura instrumentação completa em ambientes de produção.

A proposta contempla:

- Logs enviados para `stdout` / `stderr`, seguindo o padrão recomendado para workloads em Kubernetes
- Métricas expostas via endpoints HTTP (conceitual), possibilitando integração com sistemas de monitoramento
- Tracing distribuído previsto via OpenTelemetry (conceitual), permitindo rastreamento de chamadas entre microsserviços

A arquitetura é compatível com ferramentas como:

- Prometheus
- Grafana
- Jaeger / Tempo

---

## Escalabilidade

A estratégia de escalabilidade definida para a plataforma é baseada em **Horizontal Pod Autoscaler (HPA)**, alinhada ao caráter **stateless** dos microsserviços.

Essa abordagem permite que o ambiente reaja automaticamente a variações de carga, ajustando dinamicamente a quantidade de pods conforme métricas como uso de CPU ou memória, promovendo melhor utilização dos recursos do cluster.

A escolha pelo HPA é adequada para ambientes Kubernetes por ser nativa da plataforma, simples de operar e facilmente aplicável tanto em clusters locais (como Minikube) quanto em ambientes gerenciados em nuvem.

---

## Estrutura do repositório

```text
.
├── docker-compose.yml
├── gateway/
├── pedidos/
├── pagamentos/
├── estoque/
├── k8s/
│   ├── gateway/
│   ├── pedidos/
│   ├── pagamentos/
│   ├── estoque/
│   └── db/
└── .github/
    └── workflows/
```

### Descrição

- `docker-compose.yml`: ambiente local reproduzível  
- `gateway/`: API Gateway  
- `pedidos/`, `pagamentos/`, `estoque/`: microsserviços  
- `k8s/`: manifests Kubernetes  
- `.github/workflows/`: pipelines de CI/CD  

---

## Troubleshooting

### 404 via Ingress

- Verifique se o Ingress Controller está rodando
- Confirme o domínio no arquivo `hosts`
- Valide os paths configurados no Ingress

### Serviços não sobem no Compose

- Verifique variáveis de ambiente
- Confirme dependências (`depends_on`)
- Analise logs com:

```bash
docker compose logs -f
```

---

## Considerações finais

Este projeto apresenta uma proposta **fim a fim**, cobrindo desde o desenvolvimento local padronizado com Docker Compose até a orquestração em Kubernetes, aplicando práticas alinhadas a ambientes *cloud-native*.

As decisões técnicas adotadas priorizam simplicidade, clareza arquitetural e aderência a boas práticas de DevOps, como automação de ambientes, separação de responsabilidades entre serviços, configuração por variáveis de ambiente e preparação para escalabilidade horizontal.

Embora implementado em ambiente local (Minikube), o projeto foi estruturado para refletir cenários reais de produção, podendo ser facilmente adaptado para plataformas Kubernetes gerenciadas como **EKS**, **GKE** ou **AKS**, com ajustes mínimos de infraestrutura.

A solução entregue atende aos objetivos do desafio proposto, demonstrando domínio prático dos conceitos de conteinerização, orquestração, CI/CD, observabilidade e operação de sistemas distribuídos.

---

📌 **Autor:** Vinicius Rabelo Barbosa  
📌 **UniFECAF – Cloud DevOps: Orchestrating Containers and Micro Services**
