"""[A[Badapted-models-for-frontend-requirements

Revision ID: ba3aed466ed1
Revises: a4ba77a67b69
Create Date: 2024-10-27 01:39:17.406259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba3aed466ed1'
down_revision: Union[str, None] = 'a4ba77a67b69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Eliminar todos los registros existentes de la tabla ticket_messages
    op.execute("DELETE FROM ticket_messages")
    
    # Añadir la columna 'sender' como NOT NULL
    op.add_column('ticket_messages', sa.Column('sender', sa.String(), nullable=False))
    op.add_column('ticket_messages', sa.Column('email', sa.String(), nullable=False))
    op.add_column('ticket_messages', sa.Column('body', sa.Text(), nullable=False))
    op.add_column('ticket_messages', sa.Column('sent_date_time', sa.DateTime(), nullable=True))
    op.drop_column('ticket_messages', 'conversation')
    op.add_column('tickets', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('tickets', sa.Column('original_language', sa.String(), nullable=True))
    # Actualizar los registros existentes con un valor predeterminado
    op.execute("UPDATE tickets SET original_language = 'en' WHERE original_language IS NULL")
    # Cambiar la columna a NOT NULL
    op.alter_column('tickets', 'original_language',
               existing_type=sa.String(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tickets', 'original_language')
    op.drop_column('tickets', 'description')
    op.add_column('ticket_messages', sa.Column('conversation', sa.TEXT(), autoincrement=False, nullable=False))
    op.drop_column('ticket_messages', 'sent_date_time')
    op.drop_column('ticket_messages', 'body')
    op.drop_column('ticket_messages', 'email')
    op.drop_column('ticket_messages', 'sender')
    # ### end Alembic commands ###
