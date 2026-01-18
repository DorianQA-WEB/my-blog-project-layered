import asyncio
from typing import Optional

import aio_pika
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustConnection, AbstractExchange

from app.core.database import AsyncSessionLocal
from app.repositories.categories import CategoryRepository
from app.services.categories import CategoryService

import os


RABBITMQ_URL = os.getenv("RABBITMQ_URL")


async def process_category_check(
        message: AbstractIncomingMessage,
        default_exchange: AbstractExchange,
):
    """Обрабатывает входящий RPC-запрос на проверку категории."""
    async with message.process():
        response = b"false"
        try:
            category_id = int(message.body.decode())
            print(f"[.] Получен запрос на проверку category_id= {category_id}")

            async with AsyncSessionLocal() as db:
                repo = CategoryRepository(db=db)
                service = CategoryService(category_repo=repo)
                category = await service.get_category_by_id(category_id=category_id)
                if category:
                    response = b"true"
        except (ValueError, TypeError):
            print(
                f"[!] Ошибка при обработке запроса на проверку category_id: {message.body}"
            )
        except Exception as e:
            print(f"[!] Ошибка при обработке запроса: {e}")

         if message.reply_to and message.correlation_id:
             await default_exchange.publish(
                 aio_pika.Message(
                     body=response,
                     correlation_id=message.correlation_id
                 ),
                 routing_key=message.reply_to
             )
             print(f"[x] Отправлен ответ: {response.decode()}")


async def run_cunsumer():
    """Запускает consumer'а, который слушает очередь RPC-запросов."""
    connection: Optional[AbstractRobustConnection] = None
    try:
        connection = await aio_pika.connect_robust(RABBITMQ_URL)
        async with connection:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=1)

            default_exchange = await channel.default_exchange

            queue = await channel.declare_queue("category_check_queue")
            print('[+] Ожидание RPC-запросов...')

            await queue.consume(
                lambda message: process_category_check(message, default_exchange)
            )

            await asyncio.Future()
    except asyncio.CancelledError:
        print("[x] Завершение работы consumer'а...")
    finally:
        if connection and not connection.is_closed:
            await connection.close()
            print("[x] Соединение с RabbitMQ закрыто.")
