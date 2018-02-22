"""InitMigrate

Revision ID: 13fce09df3e6
Revises: 
Create Date: 2018-02-21 21:03:58.892513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13fce09df3e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('state', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('landmarks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=140), nullable=True),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['landmarks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('landmarks')
    op.drop_table('cities')
    # ### end Alembic commands ###