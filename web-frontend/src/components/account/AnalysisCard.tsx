import { Card, OverlayTrigger, Tooltip } from 'react-bootstrap';
import { BsQuestionCircle } from 'react-icons/bs';

export interface AnalysisCardProps {
  name: string;
  value: number | null;
  description?: string;
  render?: (value: number | null) => JSX.Element | null;
}

interface Props {
  metrics: AnalysisCardProps;
}

function AnalysisCard({
  metrics: {
    name,
    value,
    description,
    render = (value: number | null): JSX.Element | null => <>{value}</>
  }
}: Props): JSX.Element {
  return (
    <div className="col-sm-6 col-md-4 col-lg-3 px-1 pt-0 pb-2">
      <Card className="h-100">
        <Card.Body>
          <div className="row">
            <div className={'pr-0 ' + (description !== undefined ? 'col-9 col-xl-10' : 'col')}>
              <Card.Title className="h6 ellipsis mb-1">
                <OverlayTrigger placement="bottom" overlay={<Tooltip>{name}</Tooltip>}>
                  <span>{name}</span>
                </OverlayTrigger>
              </Card.Title>
            </div>
            <div className="col-3 col-xl-2 pl-0 text-end">
              <Card.Title className="mb-1">
                {description !== undefined ? (
                  <OverlayTrigger placement="bottom" overlay={<Tooltip>{description}</Tooltip>}>
                    <div>
                      <BsQuestionCircle className="d-inline-block align-text-top" />
                    </div>
                  </OverlayTrigger>
                ) : (
                  ''
                )}
              </Card.Title>
            </div>
          </div>
          <Card.Text className="text-end metrics-number">{render(value)}</Card.Text>
        </Card.Body>
      </Card>
    </div>
  );
}

export default AnalysisCard;
