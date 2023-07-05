from ray.core.generated.experimental import autoscaler_pb2
from ray.core.generated.instance_manager_pb2 import Instance


def get_cluster_resource_state(stub) -> autoscaler_pb2.ClusterResourceState:
    request = autoscaler_pb2.GetClusterResourceStateRequest(
        last_seen_cluster_resource_state_version=0
    )
    return stub.GetClusterResourceState(request)


class FakeCounter:
    def dec(self, *args, **kwargs):
        pass


def create_instance(
    instance_id,
    status=Instance.UNKNOWN,
    version=0,
    ray_status=Instance.RAY_STATUS_UNKOWN,
    instance_type="worker_nodes1",
):
    return Instance(
        instance_id=instance_id,
        status=status,
        version=version,
        instance_type=instance_type,
        ray_status=ray_status,
        timestamp_since_last_modified=1,
    )
