"""empty message

Revision ID: d1ec65a7aa99
Revises: 
Create Date: 2022-05-18 17:28:13.845018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1ec65a7aa99'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('author_id', sa.String(length=15), nullable=False),
    sa.Column('document_count', sa.Integer(), nullable=True),
    sa.Column('affiliation_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('author_id', name=op.f('pk_authors'))
    )
    op.create_table('authors_fullname',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.String(length=15), nullable=True),
    sa.Column('surname', sa.String(length=30), nullable=True),
    sa.Column('given_name', sa.String(length=30), nullable=True),
    sa.Column('initials', sa.String(length=30), nullable=True),
    sa.Column('is_preferred', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['authors.author_id'], name=op.f('fk_authors_fullname_author_id_authors')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_authors_fullname'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('authors_fullname')
    op.drop_table('authors')
    # ### end Alembic commands ###
