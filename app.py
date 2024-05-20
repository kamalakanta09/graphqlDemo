import graphene
from flask import Flask, request, jsonify
from azure.cosmos import CosmosClient, PartitionKey, exceptions
import os
from datetime import datetime
from cosmos_client import get_post_by_id, get_posts, insert_post

# GraphQL schema Define
class Match(graphene.ObjectType):
    matchId = graphene.String()
    id = graphene.String()
    heading = graphene.String()
    timestamp = graphene.String()  # Using String for simplicity
    summary = graphene.String()
    description = graphene.String()
    apitype = graphene.String()
    homeId = graphene.String()
    homeName = graphene.String()
    homeCode = graphene.String()
    awayId = graphene.String()
    awayName = graphene.String()
    awayCode = graphene.String()
    readTime = graphene.String()
    tag = graphene.String()
    publish = graphene.Boolean()
    enabled = graphene.Boolean()
    isModerated = graphene.Boolean()
    modDesc = graphene.String()
    approved = graphene.Boolean()
    thumbnails = graphene.String()
    images = graphene.List(graphene.String)

class MatchInput(graphene.InputObjectType):
    matchId = graphene.String()
    id = graphene.String()
    heading = graphene.String()
    timestamp = graphene.String()  # Using String for simplicity
    summary = graphene.String()
    description = graphene.String()
    apitype = graphene.String()
    homeId = graphene.String()
    homeName = graphene.String()
    homeCode = graphene.String()
    awayId = graphene.String()
    awayName = graphene.String()
    awayCode = graphene.String()
    readTime = graphene.String()
    tag = graphene.String()
    publish = graphene.Boolean()
    enabled = graphene.Boolean()
    isModerated = graphene.Boolean()
    modDesc = graphene.String()
    approved = graphene.Boolean()
    thumbnails = graphene.String()
    images = graphene.List(graphene.String)

class CreateMatch(graphene.Mutation):
    class Arguments:
        match_data = MatchInput(required=True)

    match = graphene.Field(Match)

    def mutate(self, info, match_data):
        # Convert MatchInput to dict
        match_dict = match_data.__dict__
        # Insert into Cosmos DB
        insert_post(match_dict)
        return CreateMatch(match=match_data)

class Query(graphene.ObjectType):
    matches = graphene.List(Match)
    matchById = graphene.Field(Match, id=graphene.String(required=True))

    def resolve_matches(self, info):
        return get_posts()

    def resolve_matchById(self, info, id):
        return get_post_by_id(id)
    
class Mutation(graphene.ObjectType):
    create_match = CreateMatch.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

# Flask application Create
app = Flask(__name__)

@app.route("/graphql", methods=["GET", "POST"])
def graphql_server():
    data = request.get_json()
    result = schema.execute(data.get('query'), variables=data.get('variables'))
    if result.errors:
        return jsonify({'errors': [str(error) for error in result.errors]}), 400
    return jsonify(result.data)

@app.route("/")
def home():
    return "Welcome to the GraphQL API"

if __name__ == "__main__":
    app.run(debug=True)
