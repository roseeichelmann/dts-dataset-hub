import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Nav from "../components/Nav";
import NavTile from "../components/NavTile";
import { useSocrata } from "../utils/socrata";
import { DATASETS_QUERY } from "../utils/queries";

const DESCRIPTION =
  "Datasets published and maintained by the Transportation and Public Works Department's Data and Technology Services Division.";

export default function Home() {
  const { data: datasets, error } = useSocrata({ DATASETS_QUERY });

  console.log(datasets);

  return (
    <div className="wrapper">
      <Nav isHome>
        <Row></Row>
      </Nav>
      <Container className="main">
        <Row>
          <Col xs={12} className="pt-5 text-center">
            <h1 className="text-primary fw-bold">Dataset Hub</h1>
          </Col>
        </Row>
        <Row className="mb-2 border-bottom">
          <Col xs={12} className="text-center">
            <p className="text-muted">{DESCRIPTION}</p>
          </Col>
        </Row>
        <Row className="text-dts-4 mb-4">
          {datasets &&
            datasets.map((dataset) => (
              <Col
                key={dataset.dataset_url}
                xs={12}
                md={4}
                lg={3}
                className="p-2 p-md-3 p-xl-4"
              >
                <NavTile {...dataset} />
              </Col>
            ))}
        </Row>
      </Container>
      {/* <Footer /> */}
    </div>
  );
}
