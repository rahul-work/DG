from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import osmnx
import networkx


app = FastAPI()

app.mount('/static', StaticFiles(directory="build"), name="static")

app.add_middleware(
	CORSMiddleware,
	allow_origins=[
		'http://localhost:3000'
	],
	allow_methods='*',
	allow_headers='*'
)

@app.get('/')
def root():
	return 'Hello World!'

@app.get('/exec')
def execute_command(cmd: str = ''):
	args = cmd.split()
	# return args
	if (
		args[0] == 'load'
		and args[1] == '--latitude'
		and args[2].replace('.', '', 1).isdigit()
		and args[3] == '--longitude'
		and args[4].replace('.', '', 1).isdigit()
		and args[5] == '--bbox-dist-mts'
		and args[6].replace('.', '', 1).isdigit()
	):
		simplify = False
		if len(args) == 8 and args[7] == '--simplify':
			simplify = True
		try:
			graph = osmnx.graph_from_point((float(args[2]), float(args[4])), dist=float(args[6]), simplify=simplify)
		except networkx.exception.NetworkXPointlessConcept:
			return {'status': 210, 'error_message': "No location/route in the given region!"}
		gdf_nodes, gdf_edges = osmnx.graph_to_gdfs(graph)
		nodes_geojson = gdf_nodes.to_json()
		edges_geojson = gdf_edges.to_json()
		return {'status': 200, 'nodes_geojson': nodes_geojson, 'edges_geojson': edges_geojson}
	return 'Invalid Command'