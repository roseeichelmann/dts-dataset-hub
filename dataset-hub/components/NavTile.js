import Link from "next/link";
import Card from "react-bootstrap/Card";
import { FaExternalLinkAlt } from "react-icons/fa";
// import IconLabel from "./IconLabel";

const ExternalLinkTitle = ({ title }) => (
  <div className={`d-flex flex-column`}>
    <div className="d-flex align-items-center">
      <span className="me-1">{title}</span>
      <span className="text-muted" style={{ fontSize: ".75rem" }}>
        <FaExternalLinkAlt />
      </span>
    </div>
  </div>
);

export default function NavTile({
  dataset_url,
  name,
  description,
  cover_image_url,
  external,
}) {
  console.log(cover_image_url);

  const anchorProps = external
    ? {
        target: "_blank",
        rel: "noreferrer",
      }
    : {};
  return (
    <>
      <Link className="text-decoration-none" href={dataset_url} passHref>
        <div className="text-decoration-none" {...anchorProps}>
          <Card className="h-100 nav-tile">
            {cover_image_url && (
              <Card.Img variant="top" src={cover_image_url.url} />
            )}
            <Card.Body className="p-3 lh-1">
              <Card.Title className="fw-bold fs-6 text-primary">
                {external ? <ExternalLinkTitle title={name} /> : name}
              </Card.Title>
              <span className="text-muted ">
                <small>{description}</small>
              </span>
            </Card.Body>
          </Card>
        </div>
      </Link>
    </>
  );
}
